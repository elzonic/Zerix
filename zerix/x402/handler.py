"""Handles HTTP 402 Payment Required responses using Zerix."""

import urllib.request
import urllib.error
import json
from decimal import Decimal
from ..client import ZerixClient


class X402Handler:
    """Automatically pays for HTTP 402 requests using the ZerixClient."""

    def __init__(self, client: ZerixClient):
        self.client = client

    def fetch(self, url: str) -> str:
        """
        Fetches a URL. If it returns 402, it attempts to pay and retry.
        """
        try:
            # 1. Try to access the resource normally
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.read().decode("utf-8")

        except urllib.error.HTTPError as e:
            if e.code == 402:
                # 2. Intercept HTTP 402 Payment Required
                payment_info = e.headers.get("X-Payment-Required")
                if not payment_info:
                    raise ValueError("402 Error, but no X-Payment-Required header found.")

                try:
                    data = json.loads(payment_info)
                    recipient = data["recipient"]
                    amount_usd = Decimal(str(data["amount_usd"]))
                except Exception as exc:
                    raise ValueError(f"Invalid X-Payment-Required payload: {exc}")

                # 3. Use Zerix to pay the API
                decision = self.client.transfer(to=recipient, amount_usd=amount_usd)
                
                if not decision.allowed:
                    raise PermissionError(f"Zerix denied x402 payment: {decision.reason}")

                # 4. Retry the request with proof of payment
                retry_req = urllib.request.Request(
                    url, 
                    method="GET", 
                    headers={"X-Payment-Proof": decision.reason}
                )
                with urllib.request.urlopen(retry_req, timeout=10) as retry_response:
                    return retry_response.read().decode("utf-8")
            else:
                raise
