"""Unit tests for EVMSigner (Phase 0.4)."""

from decimal import Decimal
from zerix.signers.evm import EVMSigner


def test_evm_signer_generates_valid_address():
    signer = EVMSigner()
    assert signer.address.startswith("0x")
    assert len(signer.address) == 42


def test_evm_signer_creates_transaction_hash():
    signer = EVMSigner()
    # Send $1.00 (1 ETH in testnet)
    tx_hash = signer.sign_and_send(to="0x000000000000000000000000000000000000dEaD", amount_usd=Decimal("1.0"))
    
    # The result should be a valid 66-character hex string (0x + 64 chars)
    assert tx_hash.startswith("0x")
    assert len(tx_hash) == 66
