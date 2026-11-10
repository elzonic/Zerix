"""Mock blockchain provider for local testing."""

from decimal import Decimal
from .base import BaseProvider


class MockProvider(BaseProvider):
    def __init__(self, chain_id: int = 8453, initial_balance: str = "1000.0"):
        self.chain_id = chain_id
        self.balance = Decimal(initial_balance)

    def get_balance(self, address: str) -> Decimal:
        # In a real provider, this would query an RPC node
        return self.balance

    def get_chain_id(self) -> int:
        return self.chain_id
