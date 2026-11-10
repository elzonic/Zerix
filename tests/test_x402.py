"""Unit tests for x402 Handler (Phase 2.3)."""

import json
import urllib.error
from decimal import Decimal
from unittest.mock import patch, MagicMock
from zerix import ZerixClient, PolicyEngine, SpendingCap, MockSigner, X402Handler


@patch("urllib.request.urlopen")
def test_x402_successful_payment_and_retry(mock_urlopen):
    # Mock 1: First request raises 402 with payment info
    error_402 = urllib.error.HTTPError(
        url="https://api.example.com/data",
        code=402,
        msg="Payment Required",
        hdrs={"X-Payment-Required": json.dumps({"recipient": "0xAPI", "amount_usd": "0.50"})},
        fp=None
    )
    
    # Mock 2: Retry request succeeds
    mock_retry_response = MagicMock()
    # FIX: We need to mock __enter__ because we use 'with urllib.request.urlopen(...)'
    mock_retry_response.__enter__.return_value.read.return_value = b'{"data": "premium_info"}'
    
    # Set side effects for urlopen
    mock_urlopen.side_effect = [error_402, mock_retry_response]

    # Setup Zerix
    client = ZerixClient(
        policy_engine=PolicyEngine(cap=SpendingCap(per_tx_usd=Decimal("10.0"))),
        signer=MockSigner()
    )
    handler = X402Handler(client)

    # Execute
    result = handler.fetch("https://api.example.com/data")

    assert result == '{"data": "premium_info"}'
    assert mock_urlopen.call_count == 2


@patch("urllib.request.urlopen")
def test_x402_denied_by_policy(mock_urlopen):
    error_402 = urllib.error.HTTPError(
        url="https://api.example.com/data",
        code=402,
        msg="Payment Required",
        hdrs={"X-Payment-Required": json.dumps({"recipient": "0xAPI", "amount_usd": "50.00"})}, # Exceeds cap
        fp=None
    )
    mock_urlopen.side_effect = [error_402]

    client = ZerixClient(
        policy_engine=PolicyEngine(cap=SpendingCap(per_tx_usd=Decimal("10.0"))),
        signer=MockSigner()
    )
    handler = X402Handler(client)

    import pytest
    with pytest.raises(PermissionError, match="Zerix denied x402 payment"):
        handler.fetch("https://api.example.com/data")
