"""MockSigner for local testing. Simulates a successful transaction."""

from decimal import Decimal
import uuid
from .base import BaseSigner


class MockSigner(BaseSigner):
    """Simulates signing a transaction. Useful for Phase 0 testing."""

    def sign_and_send(self, *, to: str, amount_usd: Decimal) -> str:
        # Simulate a blockchain transaction hash
        return f"0xmock_{uuid.uuid4().hex[:16]}"
