"""Unit tests for Human-in-the-Loop (HITL) threshold. Phase 1.2."""

from decimal import Decimal
from zerix import ZerixClient, PolicyEngine, SpendingCap, MockSigner, Outcome, AuditLogger
from zerix.signers.base import BaseSigner


def test_hitl_below_threshold_allowed():
    engine = PolicyEngine(cap=SpendingCap(
        per_tx_usd=Decimal("100"),
        require_human_above_usd=Decimal("50")
    ))
    client = ZerixClient(policy_engine=engine, signer=MockSigner())
    
    # $30 is below $50 threshold, allowed
    decision = client.transfer(to="0xabc", amount_usd=Decimal("30"))
    assert decision.outcome == Outcome.ALLOWED


def test_hitl_above_threshold_held():
    engine = PolicyEngine(cap=SpendingCap(
        per_tx_usd=Decimal("100"),
        require_human_above_usd=Decimal("50")
    ))
    client = ZerixClient(policy_engine=engine, signer=MockSigner())
    
    # $80 is above $50 threshold, but below $100 cap. Should be HELD.
    decision = client.transfer(to="0xabc", amount_usd=Decimal("80"))
    assert decision.outcome == Outcome.HELD
    assert "requires human approval" in decision.reason


def test_hitl_held_does_not_call_signer():
    class ExplodingSigner(BaseSigner):
        def sign_and_send(self, *, to, amount_usd):
            raise AssertionError("Signer should NOT be called when HELD!")

    engine = PolicyEngine(cap=SpendingCap(
        per_tx_usd=Decimal("100"),
        require_human_above_usd=Decimal("50")
    ))
    client = ZerixClient(policy_engine=engine, signer=ExplodingSigner())
    
    decision = client.transfer(to="0xabc", amount_usd=Decimal("80"))
    assert decision.outcome == Outcome.HELD


def test_hitl_audit_log(tmp_path):
    log_file = tmp_path / "hitl_audit.jsonl"
    engine = PolicyEngine(cap=SpendingCap(
        per_tx_usd=Decimal("100"),
        require_human_above_usd=Decimal("50")
    ))
    client = ZerixClient(
        policy_engine=engine, 
        signer=MockSigner(),
        audit_logger=AuditLogger(log_file)
    )
    
    client.transfer(to="0xabc", amount_usd=Decimal("80"))
    
    import json
    with open(log_file, "r") as f:
        log_entry = json.loads(f.readline())
        assert log_entry["action"] == "transfer_held"
        assert log_entry["amount_usd"] == "80"
