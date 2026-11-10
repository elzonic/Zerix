"""Unit tests for Webhooks (Phase 2.6)."""

from decimal import Decimal
from unittest.mock import patch, MagicMock
from zerix import ZerixClient, PolicyEngine, SpendingCap, MockSigner
from zerix.audit.webhook import WebhookNotifier


@patch("urllib.request.urlopen")
def test_webhook_sends_on_denial(mock_urlopen):
    # Setup mock
    mock_response = MagicMock()
    mock_urlopen.return_value.__enter__.return_value = mock_response

    client = ZerixClient(
        policy_engine=PolicyEngine(cap=SpendingCap(per_tx_usd=Decimal("10"))),
        signer=MockSigner(),
        webhook_url="https://example.com/webhook"
    )
    
    # Amount is $50, above $10 cap, so it gets DENIED
    client.transfer(to="0xabc", amount_usd=Decimal("50"))
    
    # Verify urlopen was called
    assert mock_urlopen.called
    args, kwargs = mock_urlopen.call_args
    req = args[0]
    
    assert req.full_url == "https://example.com/webhook"
    assert req.method == "POST"
    # Verify payload contains the denial event
    assert b"transfer_denied" in req.data


@patch("urllib.request.urlopen")
def test_webhook_sends_on_held(mock_urlopen):
    mock_response = MagicMock()
    mock_urlopen.return_value.__enter__.return_value = mock_response

    client = ZerixClient(
        policy_engine=PolicyEngine(cap=SpendingCap(
            per_tx_usd=Decimal("100"),
            require_human_above_usd=Decimal("50")
        )),
        signer=MockSigner(),
        webhook_url="https://example.com/webhook"
    )
    
    # Amount is $80, triggers HITL (HELD)
    client.transfer(to="0xabc", amount_usd=Decimal("80"))
    
    assert mock_urlopen.called
    args, kwargs = mock_urlopen.call_args
    req = args[0]
    assert b"transfer_held" in req.data
