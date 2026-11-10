"""Zerix: policy-enforcing middleware wallet for AI agents."""

from .client import ZerixClient
from .policy.decision import Decision, Outcome, PolicyDenied
from .policy.engine import PolicyEngine
from .policy.rules import Allowlist, SpendingCap, TimeWindow
from .policy.loader import load_policy_from_json
from .signers.base import BaseSigner
from .signers.mock import MockSigner
from .signers.evm import EVMSigner
from .audit.logger import AuditLogger
from .providers.base import BaseProvider
from .providers.mock import MockProvider
from .providers.rpc import JSONRPCProvider
from .automation.recurring import RecurringTransfer
from .templates import load_template

__version__ = "0.2.0"

__all__ = [
    "ZerixClient",
    "PolicyEngine",
    "SpendingCap",
    "Allowlist",
    "TimeWindow",
    "Decision",
    "Outcome",
    "PolicyDenied",
    "load_policy_from_json",
    "BaseSigner",
    "MockSigner",
    "EVMSigner",
    "AuditLogger",
    "BaseProvider",
    "MockProvider",
    "JSONRPCProvider",
    "RecurringTransfer",
    "load_template",
]
