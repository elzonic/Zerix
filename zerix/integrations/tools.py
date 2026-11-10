"""LangChain and OpenAI-compatible tools for Zerix."""

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
            
        Returns:
            A dictionary containing the outcome and reason.
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
            "description": "Transfer USDC to a recipient, subject to Zerix security policy. Always returns a status (allowed, denied, or held).",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {
                        "type": "string",
                        "description": "The blockchain address of the recipient."
                    },
                    "amount_usd": {
                        "type": "string",
                        "description": "The amount to send in USD as a string (e.g., '5.50')."
                    }
                },
                "required": ["to", "amount_usd"]
            }
        }
    }
