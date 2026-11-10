# Zerix Quickstart

Welcome to Zerix! This guide will help you integrate Zerix into your AI agent in under 5 minutes.

## Installation

pip install zerix

## Basic Setup

from decimal import Decimal
from zerix import ZerixClient, PolicyEngine, SpendingCap, MockSigner

# 1. Configure your policy (e.g., max $10 per transaction, max $50 per day)
policy = PolicyEngine(
    cap=SpendingCap(
        per_tx_usd=Decimal("10.00"),
        daily_usd=Decimal("50.00"),
        require_human_above_usd=Decimal("8.00") # HITL threshold
    )
)

# 2. Choose your signer (MockSigner for testing)
signer = MockSigner()

# 3. Initialize the client
client = ZerixClient(policy_engine=policy, signer=signer)

# 4. Execute a transfer
decision = client.transfer(to="0x123...", amount_usd=Decimal("5.00"))
print(f"Outcome: {decision.outcome.value} - {decision.reason}")

## Integrating with AI Agents

Zerix provides native schemas for popular agent frameworks:

# For LangChain
tools = client.as_langchain_tools()

# For OpenAI Function Calling
openai_tools = client.as_openai_tools()

## Viewing Audit Logs

Every decision is logged to audit.jsonl. You can view it using the built-in dashboard:

python scripts/run_dashboard.py
# Open http://localhost:8000 in your browser
