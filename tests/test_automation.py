"""Unit tests for Automation Engine (Phase 2.2)."""

from decimal import Decimal
from zerix import ZerixClient, PolicyEngine, SpendingCap, MockSigner, Outcome, RecurringTransfer


def test_recurring_transfer_executes_when_due():
    client = ZerixClient(
        policy_engine=PolicyEngine(cap=SpendingCap(per_tx_usd=Decimal("10"))),
        signer=MockSigner()
    )
    # Transfer $5 every 60 seconds
    recurring = RecurringTransfer(client, to="0xabc", amount_usd=Decimal("5"), interval_seconds=60)

    # First run (Time: 1000) -> Should execute
    decision = recurring.execute_if_due(current_time=1000.0)
    assert decision is not None
    assert decision.outcome == Outcome.ALLOWED
    assert recurring.last_run == 1000.0

    # Second run (Time: 1030) -> Only 30s passed, should NOT execute
    decision = recurring.execute_if_due(current_time=1030.0)
    assert decision is None

    # Third run (Time: 1061) -> 61s passed, should execute
    decision = recurring.execute_if_due(current_time=1061.0)
    assert decision is not None
    assert decision.outcome == Outcome.ALLOWED


def test_recurring_transfer_respects_policy():
    client = ZerixClient(
        policy_engine=PolicyEngine(cap=SpendingCap(per_tx_usd=Decimal("10"))),
        signer=MockSigner()
    )
    # Attempt to send $50, which exceeds the $10 cap
    recurring = RecurringTransfer(client, to="0xabc", amount_usd=Decimal("50"), interval_seconds=60)

    decision = recurring.execute_if_due(current_time=1000.0)
    
    # Should be denied by policy, and last_run should NOT update
    assert decision is not None
    assert decision.outcome == Outcome.DENIED
    assert recurring.last_run is None
