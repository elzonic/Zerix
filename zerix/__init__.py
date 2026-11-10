"""Zerix: policy-enforcing middleware wallet for AI agents."""

from .client import ZerixClient
from .policy.decision import Decision, Outcome, PolicyDenied
from .policy.engine import PolicyEngine
from .policy.rules import Allowlist, SpendingCap, TimeWindow
from .policy.loader import load_policy_from_json
from .signers.base import BaseSigner
from .signers.mock import MockSigner
from .signers.evm import EVMSigner
from .signers.turnkey import TurnkeySigner
from .signers.privy import PrivySigner
from .audit.logger import AuditLogger
from .providers.base import BaseProvider
from .providers.mock import MockProvider
from .providers.rpc import JSONRPCProvider
from .automation.recurring import RecurringTransfer
from .templates import load_template
from .x402.handler import X402Handler
from .database import init_db, create_user, get_user_by_api_key, generate_api_key

__version__ = "0.6.0"

__all__ = [
    "ZerixClient", "PolicyEngine", "SpendingCap", "Allowlist", "TimeWindow", "Decision", "Outcome", "PolicyDenied",
    "load_policy_from_json", "BaseSigner", "MockSigner", "EVMSigner", "TurnkeySigner", "PrivySigner",
    "AuditLogger", "BaseProvider", "MockProvider", "JSONRPCProvider", "RecurringTransfer", "load_template",
    "X402Handler", "init_db", "create_user", "get_user_by_api_key", "generate_api_key"
]
