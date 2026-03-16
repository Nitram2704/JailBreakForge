"""Secure configuration loading for JailbreakForge."""

from __future__ import annotations

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv


@dataclass
class AppConfig:
    """Application configuration loaded from environment variables."""

    provider: str = "groq"
    groq_api_key: str | None = None
    openrouter_api_key: str | None = None
    attacker_model: str = "llama-3.1-8b-instant"
    judge_model: str = "llama-3.1-8b-instant"
    max_mutations: int = 3
    target_endpoint: str | None = None
    target_model: str | None = None
    target_type: str = "openai"
    categories: list[str] = field(default_factory=list)
    output_dir: str = "reports"


def load_config() -> AppConfig:
    """Load configuration from environment variables.

    Reads all JAILBREAKFORGE_* env vars and returns an AppConfig.
    Exits with code 1 and styled error if required API key is missing.
    """
    load_dotenv()

    config = AppConfig(
        provider=os.getenv("JAILBREAKFORGE_PROVIDER", "groq"),
        groq_api_key=os.getenv("JAILBREAKFORGE_GROQ_API_KEY"),
        openrouter_api_key=os.getenv("JAILBREAKFORGE_OPENROUTER_API_KEY"),
        attacker_model=os.getenv("JAILBREAKFORGE_ATTACKER_MODEL", "llama-3.1-8b-instant"),
        judge_model=os.getenv("JAILBREAKFORGE_JUDGE_MODEL", "llama-3.1-8b-instant"),
        max_mutations=int(os.getenv("JAILBREAKFORGE_MAX_MUTATIONS", "3")),
        output_dir=os.getenv("JAILBREAKFORGE_OUTPUT_DIR", "reports"),
    )

    _validate_api_keys(config)
    return config


def get_active_api_key(config: AppConfig) -> str:
    """Return the API key for the active provider.

    Raises SystemExit with styled error if not set.
    """
    key_map = {
        "groq": config.groq_api_key,
        "openrouter": config.openrouter_api_key,
    }

    key = key_map.get(config.provider)
    if not key:
        from jailbreakforge.ui import error_console
        error_console.print(
            f"[bold red]Error:[/] API key for provider "
            f"'[yellow]{config.provider}[/yellow]' is not set.\n"
            f"Set [cyan]JAILBREAKFORGE_{config.provider.upper()}_API_KEY[/cyan] "
            f"in your .env file or environment."
        )
        raise SystemExit(1)

    return key


def _validate_api_keys(config: AppConfig) -> None:
    """Validate that at least one API key is set for the selected provider."""
    key_map = {
        "groq": config.groq_api_key,
        "openrouter": config.openrouter_api_key,
    }

    active_key = key_map.get(config.provider)
    if not active_key:
        from jailbreakforge.ui import error_console
        error_console.print(
            "[bold red]╭─ Configuration Error ─╮[/]\n"
            f"[bold red]│[/] No API key found for provider: "
            f"[yellow]{config.provider}[/yellow]\n"
            "[bold red]╰───────────────────────╯[/]\n\n"
            "[dim]Set one of the following in your .env file:[/]\n"
            "  [cyan]JAILBREAKFORGE_GROQ_API_KEY[/cyan]=your-key\n"
            "  [cyan]JAILBREAKFORGE_OPENROUTER_API_KEY[/cyan]=your-key\n\n"
            "[dim]Or switch provider with:[/]\n"
            "  [cyan]JAILBREAKFORGE_PROVIDER[/cyan]=openrouter"
        )
        raise SystemExit(1)
