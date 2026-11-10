"""Real EVM Signer using eth-account (EIP-1559)."""

from decimal import Decimal
from eth_account import Account
from .base import BaseSigner


class EVMSigner(BaseSigner):
    """Signs real EVM transactions (Ethereum, Base, Polygon, etc.)."""

    def __init__(self, private_key: str | None = None, chain_id: int = 84532):
        """
        Initializes the signer. If no private key is provided, generates a random one.
        Default chain_id is 84532 (Base Sepolia Testnet).
        """
        if private_key:
            self.account = Account.from_key(private_key)
        else:
            self.account = Account.create()
            
        self.chain_id = chain_id

    @property
    def address(self) -> str:
        return self.account.address

    def sign_and_send(self, *, to: str, amount_usd: Decimal) -> str:
        """
        Builds and signs an EIP-1559 transaction.
        Note: In a real app, you would broadcast this to an RPC node.
        Here, we return the signed transaction hash to prove it works.
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

        signed_tx = self.account.sign_transaction(transaction)
        return f"0x{signed_tx.hash.hex()}"
