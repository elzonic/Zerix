"""PolicyEngine v0 — fail-closed evaluation. Phase 0 item 0.3."""

from decimal import Decimal

from .decision import Decision, Outcome
from .rules import Allowlist, SpendingCap


class PolicyEngine:
    """
    Evaluates transactions against spending caps and allowlists.
    Fail-closed: any internal error yields DENIED.
    """

    def __init__(self, cap: SpendingCap, allowlist: Allowlist | None = None):
        self.cap = cap
        self.allowlist = allowlist or Allowlist()

    def evaluate_transfer(
        self,
        *,
        to: str,
        amount_usd: Decimal,
        daily_spent_usd: Decimal = Decimal("0"),
        weekly_spent_usd: Decimal = Decimal("0"),
    ) -> Decision:
        try:
            return self._evaluate(
                to=to,
                amount_usd=amount_usd,
                daily_spent_usd=daily_spent_usd,
                weekly_spent_usd=weekly_spent_usd,
            )
        except Exception as exc:
            return Decision(Outcome.DENIED, f"policy error (fail-closed): {exc}")

    def _evaluate(self, *, to, amount_usd, daily_spent_usd, weekly_spent_usd) -> Decision:
        if not isinstance(amount_usd, Decimal):
            amount_usd = Decimal(str(amount_usd))
        if amount_usd <= 0:
            return Decision(Outcome.DENIED, "amount must be positive")

        if amount_usd > self.cap.per_tx_usd:
            return Decision(
                Outcome.DENIED,
                f"exceeds per-tx cap (${self.cap.per_tx_usd})",
            )

        if self.cap.daily_usd is not None and daily_spent_usd + amount_usd > self.cap.daily_usd:
            return Decision(
                Outcome.DENIED,
                f"exceeds daily cap (${self.cap.daily_usd})",
            )

        if self.cap.weekly_usd is not None and weekly_spent_usd + amount_usd > self.cap.weekly_usd:
            return Decision(
                Outcome.DENIED,
                f"exceeds weekly cap (${self.cap.weekly_usd})",
            )

        if not self.allowlist.allows_recipient(to):
            return Decision(Outcome.DENIED, f"recipient {to} not in allowlist")

        return Decision(Outcome.ALLOWED, "all checks passed")
