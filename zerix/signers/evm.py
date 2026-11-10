"""Real EVM Signer using eth-account (EIP-1559)."""

import json
import urllib.request
from decimal import Decimal
from eth_account import Account
from .base import BaseSigner


class EVMSigner(BaseSigner):
    """Signs and broadcasts real EVM transactions (Ethereum, Base, Polygon, etc.)."""

    def __init__(self, private_key: str | None = None, chain_id: int = 84532, rpc_url: str | None = None):
        """
        Initializes the signer.
        If rpc_url is provided, it will broadcast the transaction to the network.
        """
        if private_key:
            self.account = Account.from_key(private_key)
        else:
            self.account = Account.create()
            
        self.chain_id = chain_id
        self.rpc_url = rpc_url

    @property
    def address(self) -> str:
        return self.account.address

    def sign_and_send(self, *, to: str, amount_usd: Decimal) -> str:
        """
        Builds, signs, and optionally broadcasts an EIP-1559 transaction.
        """
        # For testnet simulation, we assume 1 USD = 1 Native Token (ETH)
        value_wei = int(amount_usd * Decimal(10**18))

        transaction = {
            'to': to,
            'value': value_wei,
            'gas': 21000,
            'maxFeePerGas': 2000000000,      # 2 Gwei
            'maxPriorityFeePerGas': 1000000000, # 1 Gwei
            'nonce': 0,                      # In production, fetch from RPC
            'chainId': self.chain_id,
            'type': 2                        # EIP-1559
        }

        # 1. Sign locally (Fail-closed: agent never sees the key)
        signed_tx = self.account.sign_transaction(transaction)
        tx_hash = f"0x{signed_tx.hash.hex()}"

        # 2. Broadcast to the network (if RPC URL is provided)
        if self.rpc_url:
            payload = {
                "jsonrpc": "2.0",
                "method": "eth_sendRawTransaction",
                "params": [f"0x{signed_tx.raw_transaction.hex()}"],
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
                        raise ConnectionError(f"RPC Broadcast Error: {data['error']}")
                    # Return the actual network hash
                    return data["result"]
            except Exception as exc:
                raise ConnectionError(f"Failed to broadcast transaction: {exc}")

        # If no RPC is provided, just return the local hash
        return tx_hash
