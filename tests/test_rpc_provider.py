"""Unit tests for JSONRPCProvider (Phase 2.1)."""

import json
from decimal import Decimal
from unittest.mock import patch, MagicMock
from zerix.providers.rpc import JSONRPCProvider


@patch("urllib.request.urlopen")
def test_get_balance_success(mock_urlopen):
    # Simulate a JSON-RPC response for 1.5 ETH (1.5 * 10^18 Wei)
    mock_response = MagicMock()
    # 1.5 ETH in hex (wei) is 0x14d1120d7b160000
    mock_response.read.return_value = json.dumps({
        "jsonrpc": "2.0",
        "result": "0x14d1120d7b160000",
        "id": 1
    }).encode("utf-8")
    
    mock_urlopen.return_value.__enter__.return_value = mock_response

    provider = JSONRPCProvider(rpc_url="https://sepolia.base.org", chain_id=84532)
    balance = provider.get_balance("0x1234567890123456789012345678901234567890")

    assert balance == Decimal("1.5")


@patch("urllib.request.urlopen")
def test_get_balance_rpc_error(mock_urlopen):
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({
        "jsonrpc": "2.0",
        "error": {"code": -32602, "message": "Invalid address"},
        "id": 1
    }).encode("utf-8")
    
    mock_urlopen.return_value.__enter__.return_value = mock_response

    provider = JSONRPCProvider(rpc_url="https://sepolia.base.org", chain_id=84532)
    
    import pytest
    with pytest.raises(ConnectionError, match="RPC Error"):
        provider.get_balance("0xInvalidAddress")
