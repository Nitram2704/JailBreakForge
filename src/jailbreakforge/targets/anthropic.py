"""Anthropic Target Connector."""

from __future__ import annotations

import httpx

from jailbreakforge.targets.base import TargetConnector, retry_on_failure


class AnthropicTarget(TargetConnector):
    """Connector for targets using the Anthropic Messages API format."""

    @retry_on_failure(max_retries=3, base_delay=2.0)
    def send_prompt(self, prompt: str) -> str:
        """Send prompt to an Anthropic endpoint."""
        response = self.client.post(
            self.endpoint,
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1024,
            },
        )
        response.raise_for_status()

        data = response.json()
        try:
            return data["content"][0]["text"]
        except (KeyError, IndexError) as exc:
            raise ValueError(
                f"Unexpected Anthropic target response format: {data}"
            ) from exc
