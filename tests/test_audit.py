"""Unit tests for Audit Logging (Phase 1.4)."""

import json
from decimal import Decimal
from pathlib import Path
from zerix import ZerixClient, PolicyEngine, SpendingCap, MockSigner, AuditLogger


def test_audit_log_created_on_success(tmp_path):
    log_file = tmp_path / "test_audit.jsonl"
    client = ZerixClient(
        policy_engine=PolicyEngine(cap=SpendingCap(per_tx_usd=Decimal("10"))),
        signer=MockSigner(),
        audit_logger=AuditLogger(log_file)
    )
    
    client.transfer(to="0xabc", amount_usd=Decimal("5.00"))
    
    assert log_file.exists()
    
    with open(log_file, "r") as f:
        lines = f.readlines()
        assert len(lines) == 1
        
        log_entry = json.loads(lines[0])
        assert log_entry["action"] == "transfer_allowed"
        assert log_entry["to"] == "0xabc"
        assert log_entry["amount_usd"] == "5.00"
        assert "tx_hash" in log_entry
        assert "timestamp" in log_entry


def test_audit_log_created_on_policy_denial(tmp_path):
    log_file = tmp_path / "test_audit.jsonl"
    client = ZerixClient(
        policy_engine=PolicyEngine(cap=SpendingCap(per_tx_usd=Decimal("10"))),
        signer=MockSigner(),
        audit_logger=AuditLogger(log_file)
    )
    
    client.transfer(to="0xabc", amount_usd=Decimal("50.00")) # Exceeds cap
    
    with open(log_file, "r") as f:
        lines = f.readlines()
        log_entry = json.loads(lines[0])
        
        assert log_entry["action"] == "transfer_denied"
        assert "per-tx cap" in log_entry["reason"]
