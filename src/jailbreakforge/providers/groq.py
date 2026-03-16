"""Groq LLM provider — fastest free-tier inference."""

from __future__ import annotations

import httpx

from jailbreakforge.providers.base import LLMProvider, retry_on_rate_limit


class GroqProvider(LLMProvider):
    """Client for the Groq API (OpenAI-compatible format)."""

    BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

    @retry_on_rate_limit(max_retries=3, base_delay=2.0)
    def complete(self, system_prompt: str, user_prompt: str) -> str:
        """Send chat completion to Groq and return response text."""
        response = self.client.post(
            self.BASE_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.7,
                "max_tokens": 1024,
            },
        )
        response.raise_for_status()

        data = response.json()
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as exc:
            raise ValueError(
                f"Unexpected Groq response format: {data}"
            ) from exc
