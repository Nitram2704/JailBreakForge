"""Rich UI helpers for JailbreakForge terminal output."""

from __future__ import annotations

from contextlib import contextmanager

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text

console = Console()
error_console = Console(stderr=True)

BANNER = r"""
     ╦╔═╗╦╦  ╔╗ ╦═╗╔═╗╔═╗╦╔═╔═╗╔═╗╦═╗╔═╗╔═╗
     ║╠═╣║║  ╠╩╗╠╦╝║╣ ╠═╣╠╩╗╠╣ ║ ║╠╦╝║ ╦║╣
    ╚╝╩ ╩╩╩═╝╚═╝╩╚═╚═╝╩ ╩╩ ╩╚  ╚═╝╩╚═╚═╝╚═╝"""

DISCLAIMER = (
    "⚠️  This tool is for authorized security testing ONLY.\n"
    "Only test models you own or have explicit permission to test.\n"
    "Misuse may violate terms of service or applicable laws."
)


@contextmanager
def spinner(description: str = "Working..."):
    """Context manager that shows a Rich spinner for long operations."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console,
    ) as progress:
        progress.add_task(description=description, total=None)
        yield


def print_banner():
    """Print the JailbreakForge ASCII banner with version."""
    from jailbreakforge import __version__

    styled = Text(BANNER, style="bold cyan")
    console.print(styled)
    console.print(
        f"  [dim]v{__version__} — AI Security Red Teaming Framework[/dim]\n"
    )


def print_disclaimer():
    """Print ethical use disclaimer."""
    console.print(
        Panel(
            DISCLAIMER,
            title="[bold yellow]Ethical Notice[/bold yellow]",
            border_style="yellow",
            padding=(0, 2),
        )
    )
    console.print()
