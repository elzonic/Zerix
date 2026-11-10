"""Unit tests for Policy Templates (Phase 3.4)."""

import pytest
from decimal import Decimal
from zerix.templates import load_template


def test_load_api_micropayments_template():
    engine = load_template("api_micropayments")
    assert engine.cap.per_tx_usd == Decimal("0.50")
    assert engine.cap.daily_usd == Decimal("10.00")


def test_load_trading_bot_template():
    engine = load_template("trading_bot_safe")
    assert engine.cap.per_tx_usd == Decimal("50.00")
    assert engine.allowlist.allows_contract("0xUniswapV3Router") is True
    assert engine.allowlist.allows_contract("0xMalicious") is False


def test_load_invalid_template_raises_error():
    with pytest.raises(ValueError, match="not found"):
        load_template("non_existent_template")


def test_template_path_traversal_protection():
    with pytest.raises(ValueError, match="Invalid template name"):
        load_template("../secrets")
