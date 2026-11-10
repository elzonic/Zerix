"""Unit tests for Turnkey and Privy adapters (Phase 1.3)."""

import json
from decimal import Decimal
from unittest.mock import patch, MagicMock
from zerix.signers.turnkey import TurnkeySigner
from zerix.signers.privy import PrivySigner

@patch("urllib.request.urlopen")
def test_turnkey_signer(mock_urlopen):
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({"activity": {"id": "tk_12345"}}).encode("utf-8")
    mock_urlopen.return_value.__enter__.return_value = mock_response

    signer = TurnkeySigner(api_key="test", organization_id="org_1")
    tx_hash = signer.sign_and_send(to="0xabc", amount_usd=Decimal("5.0"))
    
    assert mock_urlopen.called
    assert tx_hash == "0xturnkey_tk_12345"

@patch("urllib.request.urlopen")
def test_privy_signer(mock_urlopen):
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({"hash": "pv_67890"}).encode("utf-8")
    mock_urlopen.return_value.__enter__.return_value = mock_response

    signer = PrivySigner(app_id="test", app_secret="secret", wallet_id="wal_1")
    tx_hash = signer.sign_and_send(to="0xabc", amount_usd=Decimal("5.0"))
    
    assert mock_urlopen.called
    assert tx_hash == "0xprivy_pv_67890"
