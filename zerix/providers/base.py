"""Base interface for blockchain providers (Phase 2.1)."""

from abc import ABC, abstractmethod
from decimal import Decimal


class BaseProvider(ABC):
    """Abstract interface for reading blockchain state (balances, nonces, etc.)."""

    @abstractmethod
    def get_balance(self, address: str) -> Decimal:
        """Returns the native token balance (e.g., ETH) for an address."""
        pass

    @abstractmethod
    def get_chain_id(self) -> int:
        """Returns the EIP-155 chain ID (e.g., 8453 for Base)."""
        pass
