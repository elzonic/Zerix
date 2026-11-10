"""Unit tests for the JSON Policy Loader (Phase 2.7)."""

import json
import pytest
from zerix.policy.loader import load_policy_from_json


def test_load_valid_policy(tmp_path):
    policy_file = tmp_path / "policy.json"
    policy_data = {
        "spending_cap": {"per_tx_usd": "10.00", "require_human_above_usd": "5.00"},
        "allowlist": {"recipients": ["0xABC"]},
        "time_window": {"start_hour": 9, "end_hour": 17}
    }
    with open(policy_file, "w") as f:
        json.dump(policy_data, f)

    engine = load_policy_from_json(policy_file)

    assert str(engine.cap.per_tx_usd) == "10.00"
    assert str(engine.cap.require_human_above_usd) == "5.00"
    assert engine.allowlist.allows_recipient("0xabc") is True
    assert engine.time_window.start_hour == 9


def test_load_missing_required_field(tmp_path):
    policy_file = tmp_path / "policy.json"
    policy_data = {
        "spending_cap": {"daily_usd": "50.00"}  # Missing per_tx_usd
    }
    with open(policy_file, "w") as f:
        json.dump(policy_data, f)

    with pytest.raises(ValueError, match="spending_cap.per_tx_usd is required"):
        load_policy_from_json(policy_file)


def test_load_invalid_json(tmp_path):
    policy_file = tmp_path / "policy.json"
    with open(policy_file, "w") as f:
        f.write("{ invalid json")

    with pytest.raises(ValueError, match="Invalid JSON"):
        load_policy_from_json(policy_file)
