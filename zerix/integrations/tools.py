"""LangChain, OpenAI, and MCP-compatible tools for Zerix."""

from decimal import Decimal
from typing import Any
from ..client import ZerixClient


def create_transfer_tool(client: ZerixClient):
    """Creates a tool function that an AI agent can call (LangChain-compatible)."""
    def transfer(to: str, amount_usd: str) -> dict[str, Any]:
        """
        Transfer USDC to a recipient, subject to Zerix policy.
        
        Args:
            to: The blockchain address of the recipient.
            amount_usd: The amount to send in USD (e.g., "5.00").
        """
        try:
            amount = Decimal(amount_usd)
        except Exception:
            return {"outcome": "denied", "reason": "invalid amount format"}
            
        decision = client.transfer(to=to, amount_usd=amount)
        
        return {
            "outcome": decision.outcome.value,
            "reason": decision.reason
        }
        
    return transfer


def get_openai_tool_schema() -> dict[str, Any]:
    """Returns the JSON schema for OpenAI function calling."""
    return {
        "type": "function",
        "function": {
            "name": "zerix_transfer",
            "description": "Transfer USDC to a recipient, subject to Zerix security policy.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "The recipient address."},
                    "amount_usd": {"type": "string", "description": "Amount in USD (e.g. '5.00')."}
                },
                "required": ["to", "amount_usd"]
            }
        }
    }


def get_mcp_tool_schema() -> list[dict[str, Any]]:
    """Returns the JSON schema for Model Context Protocol (MCP) tools."""
    return [{
        "name": "zerix_transfer",
        "description": "Transfer USDC to a recipient, subject to Zerix security policy.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "to": {"type": "string", "description": "The recipient address."},
                "amount_usd": {"type": "string", "description": "Amount in USD (e.g. '5.00')."}
            },
            "required": ["to", "amount_usd"]
        }
    }]
