"""Base interface for all signers (Turnkey, Privy, Mock, etc.)."""

from abc import ABC, abstractmethod
from decimal import Decimal


class BaseSigner(ABC):
    """Every signer must implement this interface."""

    @abstractmethod
    def sign_and_send(self, *, to: str, amount_usd: Decimal) -> str:
        """
        Executes the transaction and returns the transaction hash.
        Raises an exception if it fails (which the client will catch and fail-closed).
        """
        pass
