"""Target factory — creates Target instances from Config."""

from __future__ import annotations

from typing import Type

from jailbreakforge.targets.base import TargetConnector
from jailbreakforge.targets.openai import OpenAITarget
from jailbreakforge.targets.anthropic import AnthropicTarget
from jailbreakforge.targets.generic import GenericTarget
from jailbreakforge.ui import error_console

_TARGETS: dict[str, Type[TargetConnector]] = {
    "openai": OpenAITarget,
    "anthropic": AnthropicTarget,
    "generic": GenericTarget,
}


def create_target(
    target_type: str, endpoint: str, model_name: str, api_key: str
) -> TargetConnector:
    """Create a TargetConnector instance based on type.

    Args:
        target_type: Target API format ("openai", "anthropic", "generic").
        endpoint: Full URL to the target API endpoint.
        model_name: Target model identifier.
        api_key: Target API key for authentication.

    Returns:
        Configured TargetConnector instance.
        
    Raises:
        SystemExit: If target_type is invalid.
    """
    target_cls = _TARGETS.get(target_type.lower())
    if target_cls is None:
        error_console.print(
            f"[bold red]Error:[/] Unknown target type "
            f"'[yellow]{target_type}[/yellow]'.\n"
            f"Available target types: [cyan]{', '.join(_TARGETS.keys())}[/cyan]"
        )
        raise SystemExit(1)
        
    return target_cls(endpoint=endpoint, model_name=model_name, api_key=api_key)
