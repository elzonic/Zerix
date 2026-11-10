"""Unit tests for CSV Exporter (Phase 3.3)."""

import json
import csv
from zerix.audit.exporter import export_jsonl_to_csv


def test_export_jsonl_to_csv(tmp_path):
    jsonl_file = tmp_path / "audit.jsonl"
    csv_file = tmp_path / "audit.csv"

    # Create dummy data
    with open(jsonl_file, "w") as f:
        f.write(json.dumps({"timestamp": 123, "action": "transfer_allowed", "to": "0xabc", "amount_usd": "5.00", "tx_hash": "0x123"}) + "\n")
        f.write(json.dumps({"timestamp": 124, "action": "transfer_denied", "to": "0xdef", "amount_usd": "50.00", "reason": "cap exceeded"}) + "\n")

    export_jsonl_to_csv(jsonl_file, csv_file)

    assert csv_file.exists()

    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        assert len(rows) == 2
        assert rows[0]["action"] == "transfer_allowed"
        assert rows[0]["tx_hash"] == "0x123"
        assert rows[1]["action"] == "transfer_denied"
        assert rows[1]["reason"] == "cap exceeded"
