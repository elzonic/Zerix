"""Unit tests for PolicyEngine v0 — Phase 0 deliverable 0.3."""

from decimal import Decimal

from zerix.policy.decision import Outcome
from zerix.policy.engine import PolicyEngine
from zerix.policy.rules import Allowlist, SpendingCap


def _engine(**cap_kwargs) -> PolicyEngine:
    return PolicyEngine(cap=SpendingCap(per_tx_usd=Decimal("10"), **cap_kwargs))


def test_transfer_within_cap_allowed():
    assert _engine().evaluate_transfer(to="0xabc", amount_usd=Decimal("5")).outcome == Outcome.ALLOWED


def test_transfer_above_per_tx_cap_denied():
    d = _engine().evaluate_transfer(to="0xabc", amount_usd=Decimal("100"))
    assert d.outcome == Outcome.DENIED
    assert "per-tx cap" in d.reason


def test_zero_amount_denied():
    assert _engine().evaluate_transfer(to="0xabc", amount_usd=Decimal("0")).outcome == Outcome.DENIED


def test_negative_amount_denied():
    assert _engine().evaluate_transfer(to="0xabc", amount_usd=Decimal("-5")).outcome == Outcome.DENIED


def test_recipient_not_in_allowlist_denied():
    engine = PolicyEngine(
        cap=SpendingCap(per_tx_usd=Decimal("10")),
        allowlist=Allowlist(recipients={"0xALLOWED"}),
    )
    d = engine.evaluate_transfer(to="0xEVIL", amount_usd=Decimal("5"))
    assert d.outcome == Outcome.DENIED
    assert "allowlist" in d.reason


def test_recipient_in_allowlist_case_insensitive():
    engine = PolicyEngine(
        cap=SpendingCap(per_tx_usd=Decimal("10")),
        allowlist=Allowlist(recipients={"0xAbCdEf"}),
    )
    assert engine.evaluate_transfer(to="0xabcdef", amount_usd=Decimal("5")).outcome == Outcome.ALLOWED


def test_daily_cap_enforced():
    engine = PolicyEngine(cap=SpendingCap(per_tx_usd=Decimal("10"), daily_usd=Decimal("20")))
    d = engine.evaluate_transfer(
        to="0xabc", amount_usd=Decimal("10"), daily_spent_usd=Decimal("15")
    )
    assert d.outcome == Outcome.DENIED
    assert "daily cap" in d.reason


def test_fail_closed_on_internal_error():
    engine = PolicyEngine(
        cap=SpendingCap(per_tx_usd=Decimal("10")),
        allowlist=Allowlist(recipients={"0xabc"}),
    )
    d = engine.evaluate_transfer(to=None, amount_usd=Decimal("5"))  # type: ignore[arg-type]
    assert d.outcome == Outcome.DENIED
    assert "fail-closed" in d.reason
