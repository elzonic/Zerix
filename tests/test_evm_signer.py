"""Unit tests for EVMSigner (Phase 0.4)."""

import json
from decimal import Decimal
from unittest.mock import patch, MagicMock
from zerix.signers.evm import EVMSigner


def test_evm_signer_generates_valid_address():
    signer = EVMSigner()
    assert signer.address.startswith("0x")
    assert len(signer.address) == 42


def test_evm_signer_local_signing_only():
    signer = EVMSigner() # No RPC URL
    tx_hash = signer.sign_and_send(to="0x000000000000000000000000000000000000dEaD", amount_usd=Decimal("1.0"))
    
    assert tx_hash.startswith("0x")
    assert len(tx_hash) == 66


@patch("urllib.request.urlopen")
def test_evm_signer_broadcasts_to_network(mock_urlopen):
    # Setup mock response for RPC
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({
        "jsonrpc": "2.0",
        "result": "0xrealnetworkhash123",
        "id": 1
    }).encode("utf-8")
    mock_urlopen.return_value.__enter__.return_value = mock_response

    signer = EVMSigner(rpc_url="https://sepolia.base.org")
    tx_hash = signer.sign_and_send(to="0x000000000000000000000000000000000000dEaD", amount_usd=Decimal("1.0"))
    
    assert mock_urlopen.called
    assert tx_hash == "0xrealnetworkhash123"
