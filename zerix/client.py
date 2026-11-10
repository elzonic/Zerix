"""ZerixClient — the public entry point used by agents."""

from decimal import Decimal
from typing import Any

from .policy.decision import Decision, Outcome
from .policy.engine import PolicyEngine
from .signers.base import BaseSigner


class ZerixClient:
    def __init__(self, *, policy_engine: PolicyEngine, signer: BaseSigner | None = None):
        self.policy = policy_engine
        self.signer = signer

    def transfer(self, *, to: str, amount_usd: Decimal) -> Decision:
        # 1. Evaluate Policy
        decision = self.policy.evaluate_transfer(to=to, amount_usd=amount_usd)
        
        # 2. Fail-closed if denied
        if not decision.allowed:
            return decision
            
        # 3. Fail-closed if no signer
        if self.signer is None:
            return Decision(
                Outcome.DENIED,
                "no signer configured; refusing to transfer (fail-closed)",
            )

        # 4. Execute transaction (Fail-closed on error)
        try:
            tx_hash = self.signer.sign_and_send(to=to, amount_usd=amount_usd)
            return Decision(Outcome.ALLOWED, f"tx successful: {tx_hash}")
        except Exception as exc:
            return Decision(Outcome.DENIED, f"signer error (fail-closed): {exc}")

    def as_langchain_tools(self) -> list[Any]:
        """Returns a list of tools compatible with LangChain agents."""
        from .integrations.tools import create_transfer_tool
        return [create_transfer_tool(self)]
