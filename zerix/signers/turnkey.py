"""Turnkey Signer Adapter (Phase 1.3)."""

import json
import urllib.request
from decimal import Decimal
from .base import BaseSigner

class TurnkeySigner(BaseSigner):
    def __init__(self, api_key: str, organization_id: str):
        self.api_key = api_key
        self.organization_id = organization_id
        self.base_url = "https://api.turnkey.com"

    def sign_and_send(self, *, to: str, amount_usd: Decimal) -> str:
        payload = {
            "organizationId": self.organization_id,
            "type": "ACTIVITY_TYPE_SIGN_TRANSACTION",
            "parameters": {"signWith": "turnkey_wallet", "unsignedTransaction": f"Transfer {amount_usd} to {to}"}
        }
        req = urllib.request.Request(
            f"{self.base_url}/public/v1/submit/activity",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "X-API-Key": self.api_key},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
                return f"0xturnkey_{data.get('activity', {}).get('id', 'unknown')}"
        except Exception as exc:
            raise ConnectionError(f"Turnkey API error: {exc}")
