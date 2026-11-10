"""Ready-made policy templates for common agent use cases (Phase 3.4)."""

import json
from pathlib import Path
from ..policy.loader import load_policy_from_json
from ..policy.engine import PolicyEngine


def load_template(name: str) -> PolicyEngine:
    """
    Loads a pre-configured PolicyEngine based on a template name.
    Available templates: 'api_micropayments', 'trading_bot_safe'.
    """
    # Protect against directory traversal attacks
    if "/" in name or "\\" in name or ".." in name:
        raise ValueError(f"Invalid template name: {name}")

    template_dir = Path(__file__).parent
    template_path = template_dir / f"{name}.json"

    if not template_path.exists():
        available = [f.stem for f in template_dir.glob("*.json")]
        raise ValueError(f"Template '{name}' not found. Available: {available}")

    return load_policy_from_json(template_path)

__all__ = ["load_template"]
