"""LangChain-compatible tools for Zerix."""

from decimal import Decimal
from typing import Any
from ..client import ZerixClient


def create_transfer_tool(client: ZerixClient):
    """
    Creates a tool function that an AI agent can call.
    The docstring format is natively understood by LangChain.
    """
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
