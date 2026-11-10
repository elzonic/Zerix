"""Webhook notifier for Zerix events (Phase 2.6)."""

import json
import urllib.request
import urllib.error

class WebhookNotifier:
    """Sends HTTP POST requests to a webhook URL when events occur."""

    def __init__(self, url: str):
        self.url = url

    def send(self, event: dict) -> None:
        """Sends the event payload to the webhook URL."""
        if not self.url:
            return

        try:
            data = json.dumps(event).encode("utf-8")
            req = urllib.request.Request(
                self.url,
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            # Timeout 5 seconds to prevent hanging the agent
            with urllib.request.urlopen(req, timeout=5) as response:
                pass # Success
        except Exception as e:
            # Fail-safe: We log the error but do NOT crash the transaction
            print(f"Warning: Failed to send webhook to {self.url}: {e}")
