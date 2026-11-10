"""Export audit logs to CSV for compliance (Phase 3.3)."""

import csv
import json
from pathlib import Path


def export_jsonl_to_csv(input_file: str | Path, output_file: str | Path) -> None:
    """Reads a JSONL audit log and converts it to a standard CSV file."""
    in_path = Path(input_file)
    out_path = Path(output_file)

    if not in_path.exists():
        raise FileNotFoundError(f"Audit log not found: {input_file}")

    # Standard headers for compliance reports
    headers = ["timestamp", "action", "to", "amount_usd", "reason", "tx_hash"]
    rows = []

    with open(in_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                # Fill missing keys with empty strings
                row = {h: data.get(h, "") for h in headers}
                rows.append(row)
            except json.JSONDecodeError:
                continue

    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
