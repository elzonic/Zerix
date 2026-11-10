"""Unit tests for MCP integrations. Phase 1.5."""

from decimal import Decimal
from zerix import ZerixClient, PolicyEngine, SpendingCap, MockSigner


def test_as_mcp_tools_returns_schema():
    client = ZerixClient(
        policy_engine=PolicyEngine(cap=SpendingCap(per_tx_usd=Decimal("10"))),
        signer=MockSigner()
    )
    
    tools = client.as_mcp_tools()
    
    assert len(tools) == 1
    assert tools[0]["name"] == "zerix_transfer"
    assert "inputSchema" in tools[0]
    assert "to" in tools[0]["inputSchema"]["properties"]
