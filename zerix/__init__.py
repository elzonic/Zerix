"""Zerix: policy-enforcing middleware wallet for AI agents."""

from .client import ZerixClient
from .policy.decision import Decision, Outcome, PolicyDenied
from .policy.engine import PolicyEngine
from .policy.rules import Allowlist, SpendingCap

__version__ = "0.0.1"

__all__ = [
    "ZerixClient",
    "PolicyEngine",
    "SpendingCap",
    "Allowlist",
    "Decision",
    "Outcome",
    "PolicyDenied",
]
