"""PolicyEngine — fail-closed evaluation. Phase 1.1 Full Policy Engine."""

from decimal import Decimal
from datetime import datetime
from .decision import Decision, Outcome
from .rules import Allowlist, SpendingCap, TimeWindow


class PolicyEngine:
    """
    Evaluates transactions against spending caps, allowlists, and time windows.
    Fail-closed: any internal error yields DENIED.
    """

    def __init__(
        self, 
        cap: SpendingCap, 
        allowlist: Allowlist | None = None,
        time_window: TimeWindow | None = None
    ):
        self.cap = cap
        self.allowlist = allowlist or Allowlist()
        self.time_window = time_window

    def evaluate_transfer(
        self,
        *,
        to: str,
        amount_usd: Decimal,
        daily_spent_usd: Decimal = Decimal("0"),
        weekly_spent_usd: Decimal = Decimal("0"),
        current_hour: int | None = None,
    ) -> Decision:
        try:
            # Check time window first (fail-closed if outside window)
            if self.time_window:
                hour = current_hour if current_hour is not None else datetime.now().hour
                if not self.time_window.is_allowed(hour):
                    return Decision(
                        Outcome.DENIED, 
                        f"outside allowed time window ({self.time_window.start_hour}:00 - {self.time_window.end_hour}:00)"
                    )

            return self._evaluate(
                to=to,
                amount_usd=amount_usd,
                daily_spent_usd=daily_spent_usd,
                weekly_spent_usd=weekly_spent_usd,
            )
        except Exception as exc:
            return Decision(Outcome.DENIED, f"policy error (fail-closed): {exc}")

    def evaluate_contract_call(self, *, contract_address: str) -> Decision:
        """Checks if the agent is allowed to interact with a smart contract."""
        try:
            if not self.allowlist.allows_contract(contract_address):
                return Decision(Outcome.DENIED, f"contract {contract_address} not in allowlist")
            return Decision(Outcome.ALLOWED, "contract allowed")
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
