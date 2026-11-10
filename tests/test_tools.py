"""Unit tests for Agent integrations (Phase 0.5)."""

from decimal import Decimal
from zerix import ZerixClient, PolicyEngine, SpendingCap, MockSigner
from zerix.integrations.tools import create_transfer_tool


def _client() -> ZerixClient:
    return ZerixClient(
        policy_engine=PolicyEngine(cap=SpendingCap(per_tx_usd=Decimal("10"))),
        signer=MockSigner()
    )


def test_as_langchain_tools_returns_list():
    client = _client()
    tools = client.as_langchain_tools()
    
    assert len(tools) == 1
    assert callable(tools[0])


def test_transfer_tool_success():
    client = _client()
    tool = create_transfer_tool(client)
    
    result = tool(to="0xabc", amount_usd="5.00")
    
    assert result["outcome"] == "allowed"
    assert "tx successful" in result["reason"]


def test_transfer_tool_denied_by_policy():
    client = _client()
    tool = create_transfer_tool(client)
    
    # Above the $10 cap
    result = tool(to="0xabc", amount_usd="50.00")
    
    assert result["outcome"] == "denied"
    assert "per-tx cap" in result["reason"]


def test_transfer_tool_invalid_amount():
    client = _client()
    tool = create_transfer_tool(client)
    
    result = tool(to="0xabc", amount_usd="five dollars")
    
    assert result["outcome"] == "denied"
    assert result["reason"] == "invalid amount format"
