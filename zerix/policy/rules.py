"""Policy rules: spending caps and recipient allowlists (Phase 0 v0)."""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Set


@dataclass(frozen=True)
class SpendingCap:
    """Hard limits in USD. All comparisons use Decimal to avoid float drift."""

    per_tx_usd: Decimal
    daily_usd: Decimal | None = None
    weekly_usd: Decimal | None = None


@dataclass(frozen=True)
class Allowlist:
    """Empty set = no restriction on that dimension."""

    recipients: Set[str] = field(default_factory=set)
    contracts: Set[str] = field(default_factory=set)

    def allows_recipient(self, address: str) -> bool:
        if not self.recipients:
            return True
        return address.lower() in {r.lower() for r in self.recipients}
