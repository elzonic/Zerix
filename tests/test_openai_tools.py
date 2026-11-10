"""Unit tests for OpenAI integrations. Phase 1.5."""

from decimal import Decimal
from zerix import ZerixClient, PolicyEngine, SpendingCap, MockSigner


def test_as_openai_tools_returns_schema():
    client = ZerixClient(
        policy_engine=PolicyEngine(cap=SpendingCap(per_tx_usd=Decimal("10"))),
        signer=MockSigner()
    )
    
    tools = client.as_openai_tools()
    
    assert len(tools) == 1
    assert tools[0]["type"] == "function"
    assert tools[0]["function"]["name"] == "zerix_transfer"
