"""Abstract base class for LLM providers with retry logic."""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Callable

import httpx

from jailbreakforge.ui import error_console


def retry_on_rate_limit(max_retries: int = 3, base_delay: float = 1.0):
    """Decorator: exponential backoff on 429 rate-limit responses."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except httpx.HTTPStatusError as exc:
                    if exc.response.status_code == 429 and attempt < max_retries:
                        delay = base_delay * (2 ** attempt)
                        error_console.print(
                            f"[yellow]⏳ Rate limited. "
                            f"Retrying in {delay:.0f}s "
                            f"(attempt {attempt + 1}/{max_retries})...[/]"
                        )
                        time.sleep(delay)
                        continue
                    raise
            return None  # unreachable, satisfies type checker

        return wrapper

    return decorator


class LLMProvider(ABC):
    """Abstract base class for all LLM providers."""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.client = httpx.Client(timeout=30.0)

    @abstractmethod
    def complete(self, system_prompt: str, user_prompt: str) -> str:
        """Send a chat completion request and return the response text.

        Args:
            system_prompt: System-level instructions.
            user_prompt: User message content.

        Returns:
            Model response text.
        """

    def close(self):
        """Close the HTTP client."""
        self.client.close()
