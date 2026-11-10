"""ZerixClient — the public entry point used by agents."""

from decimal import Decimal
from typing import Any

from .policy.decision import Decision, Outcome
from .policy.engine import PolicyEngine
from .signers.base import BaseSigner
from .audit.logger import AuditLogger
from .audit.webhook import WebhookNotifier
from .providers.base import BaseProvider


class ZerixClient:
    def __init__(
        self, 
        *, 
        policy_engine: PolicyEngine, 
        signer: BaseSigner | None = None,
        audit_logger: AuditLogger | None = None,
        provider: BaseProvider | None = None,
        webhook_url: str | None = None
    ):
        self.policy = policy_engine
        self.signer = signer
        self.audit = audit_logger or AuditLogger()
        self.provider = provider
        self.webhook = WebhookNotifier(webhook_url) if webhook_url else None

    def _trigger_webhook(self, action: str, to: str, amount_usd: Decimal, reason: str):
        if self.webhook:
            self.webhook.send({
                "event": action,
                "to": to,
                "amount_usd": str(amount_usd),
                "reason": reason
            })

    def transfer(self, *, to: str, amount_usd: Decimal) -> Decision:
        decision = self.policy.evaluate_transfer(to=to, amount_usd=amount_usd)
        
        if decision.outcome == Outcome.DENIED:
            self.audit.log({"action": "transfer_denied", "to": to, "amount_usd": str(amount_usd), "reason": decision.reason})
            self._trigger_webhook("transfer_denied", to, amount_usd, decision.reason)
            return decision

        if decision.outcome == Outcome.HELD:
            self.audit.log({"action": "transfer_held", "to": to, "amount_usd": str(amount_usd), "reason": decision.reason})
            self._trigger_webhook("transfer_held", to, amount_usd, decision.reason)
            return decision
            
        if self.signer is None:
            reason = "no signer configured; refusing to transfer (fail-closed)"
            self.audit.log({"action": "transfer_denied", "to": to, "amount_usd": str(amount_usd), "reason": reason})
            self._trigger_webhook("transfer_denied", to, amount_usd, reason)
            return Decision(Outcome.DENIED, reason)

        try:
            if self.provider:
                balance = self.provider.get_balance("agent_wallet")
                if balance <= 0:
                    raise ValueError("Insufficient on-chain balance")

            tx_hash = self.signer.sign_and_send(to=to, amount_usd=amount_usd)
            self.audit.log({"action": "transfer_allowed", "to": to, "amount_usd": str(amount_usd), "tx_hash": tx_hash})
            # Note: We typically don't trigger webhooks for success, only alerts. 
            # But we could if needed.
            return Decision(Outcome.ALLOWED, f"tx successful: {tx_hash}")
            
        except Exception as exc:
            reason = f"signer/provider error (fail-closed): {exc}"
            self.audit.log({"action": "transfer_denied", "to": to, "amount_usd": str(amount_usd), "reason": reason})
            self._trigger_webhook("transfer_denied", to, amount_usd, reason)
            return Decision(Outcome.DENIED, reason)

    def as_langchain_tools(self) -> list[Any]:
        from .integrations.tools import create_transfer_tool
        return [create_transfer_tool(self)]

    def as_openai_tools(self) -> list[dict[str, Any]]:
        from .integrations.tools import get_openai_tool_schema
        return [get_openai_tool_schema()]

    def as_mcp_tools(self) -> list[dict[str, Any]]:
        from .integrations.tools import get_mcp_tool_schema
        return get_mcp_tool_schema()
