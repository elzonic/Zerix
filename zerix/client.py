"""ZerixClient — the public entry point used by agents."""

from decimal import Decimal
from typing import Any

from .policy.decision import Decision, Outcome
from .policy.engine import PolicyEngine
from .signers.base import BaseSigner
from .audit.logger import AuditLogger


class ZerixClient:
    def __init__(
        self, 
        *, 
        policy_engine: PolicyEngine, 
        signer: BaseSigner | None = None,
        audit_logger: AuditLogger | None = None
    ):
        self.policy = policy_engine
        self.signer = signer
        self.audit = audit_logger or AuditLogger()

    def transfer(self, *, to: str, amount_usd: Decimal) -> Decision:
        decision = self.policy.evaluate_transfer(to=to, amount_usd=amount_usd)
        
        # 1. Fail-closed if DENIED
        if decision.outcome == Outcome.DENIED:
            self.audit.log({
                "action": "transfer_denied",
                "to": to,
                "amount_usd": str(amount_usd),
                "reason": decision.reason
            })
            return decision

        # 2. Handle HITL (HELD) - Phase 1.2
        if decision.outcome == Outcome.HELD:
            self.audit.log({
                "action": "transfer_held",
                "to": to,
                "amount_usd": str(amount_usd),
                "reason": decision.reason
            })
            return decision
            
        # 3. Fail-closed if no signer
        if self.signer is None:
            reason = "no signer configured; refusing to transfer (fail-closed)"
            self.audit.log({
                "action": "transfer_denied",
                "to": to,
                "amount_usd": str(amount_usd),
                "reason": reason
            })
            return Decision(Outcome.DENIED, reason)

        # 4. Execute transaction
        try:
            tx_hash = self.signer.sign_and_send(to=to, amount_usd=amount_usd)
            self.audit.log({
                "action": "transfer_allowed",
                "to": to,
                "amount_usd": str(amount_usd),
                "tx_hash": tx_hash
            })
            return Decision(Outcome.ALLOWED, f"tx successful: {tx_hash}")
            
        except Exception as exc:
            reason = f"signer error (fail-closed): {exc}"
            self.audit.log({
                "action": "transfer_denied",
                "to": to,
                "amount_usd": str(amount_usd),
                "reason": reason
            })
            return Decision(Outcome.DENIED, reason)

    def as_langchain_tools(self) -> list[Any]:
        from .integrations.tools import create_transfer_tool
        return [create_transfer_tool(self)]
