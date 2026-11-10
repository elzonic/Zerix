"""Zerix: policy-enforcing middleware wallet for AI agents."""

from .client import ZerixClient
from .policy.decision import Decision, Outcome, PolicyDenied
from .policy.engine import PolicyEngine
from .policy.rules import Allowlist, SpendingCap
from .signers.base import BaseSigner
from .signers.mock import MockSigner
from .audit.logger import AuditLogger

__version__ = "0.0.1"

__all__ = [
    "ZerixClient",
    "PolicyEngine",
    "SpendingCap",
    "Allowlist",
    "Decision",
    "Outcome",
    "PolicyDenied",
    "BaseSigner",
    "MockSigner",
    "AuditLogger",
]
