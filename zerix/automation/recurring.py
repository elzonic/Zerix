"""Recurring transfers for agents (e.g., DCA, subscriptions)."""

import time
from decimal import Decimal
from ..client import ZerixClient
from ..policy.decision import Decision


class RecurringTransfer:
    """Handles a transfer that occurs at a fixed interval."""

    def __init__(self, client: ZerixClient, to: str, amount_usd: Decimal, interval_seconds: int):
        self.client = client
        self.to = to
        self.amount_usd = amount_usd
        self.interval_seconds = interval_seconds
        self.last_run: float | None = None

    def execute_if_due(self, current_time: float | None = None) -> Decision | None:
        """Executes the transfer if the interval has passed."""
        now = current_time if current_time is not None else time.time()

        if self.last_run is None or (now - self.last_run >= self.interval_seconds):
            # Attempt transfer (Policy Engine will still deny/held if limits are breached)
            decision = self.client.transfer(to=self.to, amount_usd=self.amount_usd)
            
            # If it was allowed, we update the last_run timestamp
            if decision.allowed:
                self.last_run = now
                
            return decision
            
        return None  # Not due yet
