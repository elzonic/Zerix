"""Decision types returned by the policy engine."""

from dataclasses import dataclass
from enum import Enum


class Outcome(str, Enum):
    ALLOWED = "allowed"
    DENIED = "denied"
    HELD = "held"  # reserved for Phase 1 HITL


class PolicyDenied(Exception):
    """Raised when a policy decision is DENIED and the caller wants an exception."""


@dataclass(frozen=True)
class Decision:
    outcome: Outcome
    reason: str = ""

    @property
    def allowed(self) -> bool:
        return self.outcome == Outcome.ALLOWED

    def __bool__(self) -> bool:
        # Fail-closed: only ALLOWED is truthy. HELD is NOT truthy.
        return self.outcome == Outcome.ALLOWED
