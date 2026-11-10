"""Loads Zerix policies from external JSON files (Phase 2.7)."""

import json
from decimal import Decimal
from pathlib import Path
from .engine import PolicyEngine
from .rules import Allowlist, SpendingCap, TimeWindow


def load_policy_from_json(file_path: str | Path) -> PolicyEngine:
    """
    Reads a JSON file and returns a configured PolicyEngine.
    Fail-closed: raises ValueError if the JSON is invalid or missing required fields.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Policy file not found: {file_path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in policy file: {exc}")

    # 1. Parse SpendingCap (Required)
    cap_data = data.get("spending_cap", {})
    if "per_tx_usd" not in cap_data:
        raise ValueError("spending_cap.per_tx_usd is required")

    cap = SpendingCap(
        per_tx_usd=Decimal(str(cap_data["per_tx_usd"])),
        daily_usd=Decimal(str(cap_data["daily_usd"])) if "daily_usd" in cap_data else None,
        weekly_usd=Decimal(str(cap_data["weekly_usd"])) if "weekly_usd" in cap_data else None,
        require_human_above_usd=Decimal(str(cap_data["require_human_above_usd"])) if "require_human_above_usd" in cap_data else None,
    )

    # 2. Parse Allowlist (Optional)
    allowlist = None
    if "allowlist" in data:
        allow_data = data["allowlist"]
        allowlist = Allowlist(
            recipients=set(allow_data.get("recipients", [])),
            contracts=set(allow_data.get("contracts", []))
        )

    # 3. Parse TimeWindow (Optional)
    time_window = None
    if "time_window" in data:
        tw_data = data["time_window"]
        time_window = TimeWindow(
            start_hour=int(tw_data["start_hour"]),
            end_hour=int(tw_data["end_hour"])
        )

    return PolicyEngine(cap=cap, allowlist=allowlist, time_window=time_window)
