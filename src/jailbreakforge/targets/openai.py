"""OpenAI-compatible Target Connector."""

from __future__ import annotations

import httpx

from jailbreakforge.targets.base import TargetConnector, retry_on_failure


class OpenAITarget(TargetConnector):
    """Connector for targets using the OpenAI Chat Completions API format."""

    @retry_on_failure(max_retries=3, base_delay=2.0)
    def send_prompt(self, prompt: str) -> str:
        """Send prompt to an OpenAI-compatible endpoint."""
        response = self.client.post(
            self.endpoint,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                # Avoid max_tokens if possible to get full responses
            },
        )
        response.raise_for_status()

        data = response.json()
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as exc:
            raise ValueError(
                f"Unexpected OpenAI target response format: {data}"
            ) from exc
