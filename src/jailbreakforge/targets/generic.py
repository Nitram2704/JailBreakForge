"""Generic HTTP POST Target Connector."""

from __future__ import annotations

import httpx

from jailbreakforge.targets.base import TargetConnector, retry_on_failure


class GenericTarget(TargetConnector):
    """Connector for generic targets expecting {"prompt": "..."} format."""

    @retry_on_failure(max_retries=3, base_delay=2.0)
    def send_prompt(self, prompt: str) -> str:
        """Send prompt as a simple JSON payload."""
        headers = {"Content-Type": "application/json"}
        if self.api_key and self.api_key.lower() != "none":
            headers["Authorization"] = f"Bearer {self.api_key}"

        response = self.client.post(
            self.endpoint,
            headers=headers,
            json={"prompt": prompt},
        )
        response.raise_for_status()

        data = response.json()
        
        # Try to guess where the response is based on common patterns
        if isinstance(data, dict):
            if "response" in data:
                return data["response"]
            if "text" in data:
                return data["text"]
            if "output" in data:
                return data["output"]
            
        # Fallback to stringifying the whole dict if we can't guess
        return str(data)
