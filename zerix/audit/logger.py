"""Structured JSONL audit logger (Phase 1.4)."""

import json
import time
from pathlib import Path
from typing import Any


class AuditLogger:
    """Appends every decision to a JSONL file for security auditing."""

    def __init__(self, log_file: str | Path = "audit.jsonl"):
        self.log_file = Path(log_file)

    def log(self, event: dict[str, Any]) -> None:
        """Write a single structured event to the log file."""
        # Add timestamp
        event_record = {
            "timestamp": time.time(),
            **event
        }
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(event_record) + "\n")
        except Exception:
            # Fail-closed: if we cannot write the audit log, we should ideally 
            # block the transaction. For now, we print to stderr.
            print(f"CRITICAL: Failed to write audit log for event: {event}")
