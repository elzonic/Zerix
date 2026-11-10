"""Privy Signer Adapter (Phase 1.3)."""

import json
import urllib.request
from decimal import Decimal
from .base import BaseSigner

class PrivySigner(BaseSigner):
    def __init__(self, app_id: str, app_secret: str, wallet_id: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.wallet_id = wallet_id
        self.base_url = "https://auth.privy.io/api/v1"

    def sign_and_send(self, *, to: str, amount_usd: Decimal) -> str:
        payload = {"wallet_id": self.wallet_id, "to": to, "value": str(amount_usd), "chain": "base"}
        req = urllib.request.Request(
            f"{self.base_url}/wallets/{self.wallet_id}/transfer",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "privy-app-id": self.app_id,
                "Authorization": f"Basic {self.app_secret}"
            },
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
                return f"0xprivy_{data.get('hash', 'unknown')}"
        except Exception as exc:
            raise ConnectionError(f"Privy API error: {exc}")
