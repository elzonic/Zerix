"""Unit tests for ZerixClient integration with MockSigner."""

from decimal import Decimal
import pytest
from zerix import ZerixClient, PolicyEngine, SpendingCap, MockSigner, Outcome
from zerix.signers.base import BaseSigner


def _engine() -> PolicyEngine:
    return PolicyEngine(cap=SpendingCap(per_tx_usd=Decimal("10")))


def test_transfer_success_with_mock_signer():
    client = ZerixClient(policy_engine=_engine(), signer=MockSigner())
    decision = client.transfer(to="0xabc", amount_usd=Decimal("5"))
    
    assert decision.outcome == Outcome.ALLOWED
    assert "tx successful" in decision.reason
    assert "0xmock_" in decision.reason


def test_transfer_denied_by_policy_does_not_call_signer():
    # Create a signer that raises an error if called
    class ExplodingSigner(BaseSigner):
        def sign_and_send(self, *, to, amount_usd):
            raise AssertionError("Signer should NOT be called when policy denies!")

    client = ZerixClient(policy_engine=_engine(), signer=ExplodingSigner())
    decision = client.transfer(to="0xabc", amount_usd=Decimal("100"))  # Above cap
    
    assert decision.outcome == Outcome.DENIED
    assert "per-tx cap" in decision.reason


def test_transfer_fails_closed_if_no_signer():
    client = ZerixClient(policy_engine=_engine(), signer=None)
    decision = client.transfer(to="0xabc", amount_usd=Decimal("5"))
    
    assert decision.outcome == Outcome.DENIED
    assert "no signer" in decision.reason


def test_transfer_fails_closed_if_signer_throws():
    class BrokenSigner(BaseSigner):
        def sign_and_send(self, *, to, amount_usd):
            raise ConnectionError("Network disconnected")

    client = ZerixClient(policy_engine=_engine(), signer=BrokenSigner())
    decision = client.transfer(to="0xabc", amount_usd=Decimal("5"))
    
    assert decision.outcome == Outcome.DENIED
    assert "signer/provider error (fail-closed)" in decision.reason
    assert "Network disconnected" in decision.reason
