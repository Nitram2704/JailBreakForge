"""Provider factory — creates LLM provider instances from config."""

from __future__ import annotations

from jailbreakforge.providers.base import LLMProvider
from jailbreakforge.providers.groq import GroqProvider
from jailbreakforge.providers.openrouter import OpenRouterProvider

_PROVIDERS: dict[str, type[LLMProvider]] = {
    "groq": GroqProvider,
    "openrouter": OpenRouterProvider,
}


def create_provider(provider_name: str, api_key: str, model: str) -> LLMProvider:
    """Create an LLM provider instance from its name, key, and model.

    Args:
        provider_name: Provider identifier (groq, openrouter).
        api_key: API key for authentication.
        model: Model identifier string.

    Returns:
        Configured LLMProvider instance.

    Raises:
        ValueError: If provider_name is not recognized.
    """
    provider_cls = _PROVIDERS.get(provider_name)
    if provider_cls is None:
        raise ValueError(
            f"Unknown provider: '{provider_name}'. "
            f"Available: {list(_PROVIDERS.keys())}"
        )
    return provider_cls(api_key=api_key, model=model)
