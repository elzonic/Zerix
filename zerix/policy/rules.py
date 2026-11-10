"""Policy rules: spending caps, allowlists, and time windows."""

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

    def allows_contract(self, address: str) -> bool:
        if not self.contracts:
            return True
        return address.lower() in {c.lower() for c in self.contracts}


@dataclass(frozen=True)
class TimeWindow:
    """Restricts when transactions can occur (0-23 hours)."""

    start_hour: int
    end_hour: int

    def is_allowed(self, current_hour: int) -> bool:
        if self.start_hour <= self.end_hour:
            return self.start_hour <= current_hour <= self.end_hour
        # Handles overnight windows (e.g., 22:00 to 04:00)
        return current_hour >= self.start_hour or current_hour <= self.end_hour
