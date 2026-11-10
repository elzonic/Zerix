"""Real Web3 JSON-RPC Provider (Phase 2.1 implementation)."""

import json
import urllib.request
from decimal import Decimal
from .base import BaseProvider


class JSONRPCProvider(BaseProvider):
    """Connects to a real blockchain node via JSON-RPC."""

    def __init__(self, rpc_url: str, chain_id: int):
        self.rpc_url = rpc_url
        self.chain_id = chain_id

    def get_chain_id(self) -> int:
        return self.chain_id

    def get_balance(self, address: str) -> Decimal:
        """Fetches the native token balance (e.g., ETH) using eth_getBalance."""
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getBalance",
            "params": [address, "latest"],
            "id": 1
        }
        
        req = urllib.request.Request(
            self.rpc_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
                
                if "error" in data:
                    raise ValueError(f"RPC Error: {data['error']}")
                
                # Result is in Wei (Hex). Convert to Decimal (Ether)
                wei_hex = data["result"]
                wei = int(wei_hex, 16)
                ether = Decimal(wei) / Decimal(10**18)
                return ether
                
        except Exception as exc:
            raise ConnectionError(f"Failed to fetch balance from RPC: {exc}")
