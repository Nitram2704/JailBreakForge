"""JailbreakForge CLI — Typer entrypoint."""

from __future__ import annotations

from typing import Optional

import typer

from jailbreakforge import __version__
from jailbreakforge.config import load_config
from jailbreakforge.ui import console, print_banner, print_disclaimer

app = typer.Typer(
    name="jailbreakforge",
    help="🔒 JailbreakForge — AI Security Red Teaming Framework",
    no_args_is_help=True,
)


@app.command()
def run(
    target: str = typer.Option(..., "--target", "-t", help="Target API endpoint URL"),
    model: str = typer.Option(..., "--model", "-m", help="Target model name"),
    target_key: str = typer.Option(..., "--target-key", "-k", help="Target API key"),
    target_type: str = typer.Option("openai", "--type", help="openai | anthropic | generic"),
    name: str = typer.Option("target", "--name", "-n", help="Human-friendly target name"),
    categories: Optional[str] = typer.Option(None, "--categories", "-c", help="Comma-separated categories"),
    max_mutations: int = typer.Option(3, "--max-mutations", help="Max mutations per seed (1-5)"),
    provider: Optional[str] = typer.Option(None, "--provider", "-p", help="groq | openrouter"),
    output_dir: str = typer.Option("reports", "--output", "-o", help="Report output directory"),
):
    """🔒 Run a security audit against a target AI model."""
    import uuid
    from datetime import datetime
    
    from jailbreakforge.attacker import AttackerAgent
    from jailbreakforge.config import get_active_api_key
    from jailbreakforge.db import Database
    from jailbreakforge.judge import JudgeAgent
    from jailbreakforge.models import RunConfig
    from jailbreakforge.pipeline import Pipeline
    from jailbreakforge.providers.factory import create_provider
    from jailbreakforge.reporter import ReportGenerator
    from jailbreakforge.seeds import list_categories
    from jailbreakforge.targets.factory import create_target
    from jailbreakforge.ui import spinner
    
    print_banner()
    print_disclaimer()

    config = load_config()

    if provider:
        config.provider = provider
    
    # Parse categories
    cat_list = categories.split(",") if categories else list_categories()
    
    run_id = str(uuid.uuid4())
    run_config = RunConfig(
        run_id=run_id,
        target_name=name,
        target_endpoint=target,
        target_model=model,
        categories=cat_list,
        max_mutations=max_mutations,
        provider=config.provider,
        attacker_model=config.attacker_model,
        judge_model=config.judge_model,
        started_at=datetime.utcnow().isoformat()
    )

    with spinner("Initializing components..."):
        api_key = get_active_api_key(config)
        attacker_provider = create_provider(config.provider, api_key, config.attacker_model)
        judge_provider = create_provider(config.provider, api_key, config.judge_model)
        target_conn = create_target(target_type, target, model, target_key)
        
        attacker = AttackerAgent(attacker_provider)
        judge = JudgeAgent(judge_provider)
        db = Database()
        reporter = ReportGenerator(output_dir)
        
        pipeline = Pipeline(config, attacker, target_conn, judge, db, reporter)

    summary, report_path = pipeline.execute(run_config)
    
    # Cleanup
    db.close()
    target_conn.close()
    attacker_provider.close()
    judge_provider.close()

    # Print results summary
    if report_path:
        rating, emoji = ReportGenerator.get_rating(summary.security_score)
        console.print(f"\n{emoji} [bold]Security Score:[/] {summary.security_score:.1f}/100 ({rating})")
        console.print(f"📊 [dim]Attacks:[/] {summary.total_attacks} | [green]🟢 Blocked:[/] {summary.total_blocked} | [red]🔴 Vulnerable:[/] {summary.total_vulnerable} | [yellow]🟡 Partial:[/] {summary.total_partial}")
        console.print(f"📄 [bold]Report generated:[/] [cyan]{report_path}[/cyan]\n")


@app.command()
def version():
    """Show version information."""
    console.print(f"[bold cyan]JailbreakForge[/bold cyan] v{__version__}")


@app.command(name="list-categories")
def list_categories_cmd():
    """List available attack categories."""
    console.print("[bold]Available Attack Categories:[/bold]\n")
    categories = [
        ("roleplay", "Alternate identity assignment (DAN, Evil AI)"),
        ("character_hijacking", "Emotional manipulation via characters"),
        ("encoding", "Base64/ROT13 encoded instructions"),
        ("logical_injection", "Reasoning chain exploitation"),
        ("system_prompt_extraction", "System instruction extraction attempts"),
        ("hypothetical_scenario", "Harmful requests framed as fiction"),
        ("multiturn_escalation", "Gradual boundary pushing"),
        ("language_switching", "Alternate language evasion"),
    ]
    for cat, desc in categories:
        console.print(f"  [cyan]•[/cyan] [bold]{cat}[/bold] — {desc}")
    console.print(f"\n[dim]Total: {len(categories)} categories[/dim]")


if __name__ == "__main__":
    app()
