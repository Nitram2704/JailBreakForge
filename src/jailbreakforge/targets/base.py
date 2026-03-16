"""Abstract base class for Target Connectors."""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Callable

import httpx

from jailbreakforge.ui import error_console


def retry_on_failure(max_retries: int = 3, base_delay: float = 1.0):
    """Decorator: exponential backoff for 429 and 50x responses."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except httpx.HTTPError as exc:
                    # Retry on 429 (Rate Limit) or 500+ (Server Error)
                    status = getattr(getattr(exc, "response", None), "status_code", None)
                    if status in (429, 500, 502, 503, 504) and attempt < max_retries:
                        delay = base_delay * (2 ** attempt)
                        error_console.print(
                            f"[dim yellow]⏳ Target rate limited/unavailable (HTTP {status}). "
                            f"Retrying in {delay:.0f}s...[/]"
                        )
                        time.sleep(delay)
                        continue
                    # On final attempt or non-retriable error, raise
                    raise
            return None

        return wrapper

    return decorator


class TargetConnector(ABC):
    """Abstract base class for all Target AI models."""

    def __init__(self, endpoint: str, model_name: str, api_key: str):
        self.endpoint = endpoint
        self.model_name = model_name
        self.api_key = api_key
        self.client = httpx.Client(timeout=45.0)  # Targets might be slow

    @abstractmethod
    def send_prompt(self, prompt: str) -> str:
        """Send an attack prompt to the target and return its response.

        Args:
            prompt: The full attack payload.

        Returns:
            The raw string response from the target model.
        """

    def close(self):
        """Close the HTTP client."""
        self.client.close()
