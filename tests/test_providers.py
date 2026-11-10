"""Unit tests for Provider Adapters (Phase 2.1)."""

from decimal import Decimal
from zerix import ZerixClient, PolicyEngine, SpendingCap, MockSigner, MockProvider, Outcome


def test_mock_provider_chain_id():
    provider = MockProvider(chain_id=1) # Ethereum Mainnet
    assert provider.get_chain_id() == 1


def test_mock_provider_balance():
    provider = MockProvider(initial_balance="500.5")
    assert provider.get_balance("0xabc") == Decimal("500.5")


def test_client_fails_closed_if_provider_balance_zero():
    client = ZerixClient(
        policy_engine=PolicyEngine(cap=SpendingCap(per_tx_usd=Decimal("10"))),
        signer=MockSigner(),
        provider=MockProvider(initial_balance="0") # Zero balance
    )
    
    decision = client.transfer(to="0xabc", amount_usd=Decimal("5"))
    
    # Should fail because balance is 0
    assert decision.outcome == Outcome.DENIED
    assert "Insufficient on-chain balance" in decision.reason
