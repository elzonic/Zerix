"""ZerixClient — the public entry point used by agents.

Phase 0.2 stub. Signer execution lands in Phase 0.4.
"""

from decimal import Decimal

from .policy.decision import Decision, Outcome
from .policy.engine import PolicyEngine


class ZerixClient:
    def __init__(self, *, policy_engine: PolicyEngine, signer=None):
        self.policy = policy_engine
        self.signer = signer

    def transfer(self, *, to: str, amount_usd: Decimal) -> Decision:
        decision = self.policy.evaluate_transfer(to=to, amount_usd=amount_usd)
        if not decision.allowed:
            return decision
        if self.signer is None:
            return Decision(
                Outcome.DENIED,
                "no signer configured; refusing to transfer (fail-closed)",
            )
        raise NotImplementedError("Signer execution: Phase 0.4")
