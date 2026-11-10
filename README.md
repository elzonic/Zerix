<div align="center">
  <h1>🛡️ Zerix</h1>
  <p><b>Policy-enforcing middleware wallet for AI agents.</b></p>
  
  [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
  [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
  [![Version](https://img.shields.io/badge/version-0.2.0-green.svg)]()
  
  <p>Zerix sits between your AI agent and the blockchain. It ensures that no matter how smart (or easily manipulated) your agent is, it can never drain your funds or interact with malicious contracts.</p>
</div>

---

## ✨ Features

- **Fail-Closed Policy Engine:** Spending caps (per-tx, daily, weekly), recipient/contract allowlists, and time windows.
- **Human-in-the-Loop (HITL):** Transactions above a specific threshold are `HELD` for manual approval.
- **Web3 Native:** Generates real EIP-1559 transactions and broadcasts them to Base, Ethereum, or any EVM chain.
- **Zero-Dependency UI:** A beautiful, read-only dashboard to monitor agent activity in real-time.
- **Framework Agnostic:** Native tool schemas for LangChain, OpenAI Function Calling, and MCP.
- **Audit Logging:** Every decision is recorded in a structured JSONL format (exportable to CSV).

## 🏗️ Architecture

~~~text
[ AI Agent ] ---> [ Zerix Client ] ---> [ Blockchain (Base/EVM) ]
                         |
                         +-- [ Policy Engine ] (Caps, Allowlists, Time)
                         +-- [ HITL Engine ]   (Holds large transactions)
                         +-- [ EVM Signer ]    (Securely holds private keys)
                         +-- [ Audit Logger ]  (JSONL & Dashboard)
~~~

## 🚀 Quickstart

### 1. Installation

~~~bash
pip install zerix
~~~

### 2. Basic Usage (Simulation)

~~~python
from decimal import Decimal
from zerix import ZerixClient, PolicyEngine, SpendingCap, MockSigner

# 1. Configure Policy (Max $10 per tx, hold above $5)
policy = PolicyEngine(
    cap=SpendingCap(
        per_tx_usd=Decimal("10.00"),
        require_human_above_usd=Decimal("5.00")
    )
)

# 2. Initialize Client
client = ZerixClient(policy_engine=policy, signer=MockSigner())

# 3. Execute Transfer
decision = client.transfer(to="0x123...", amount_usd=Decimal("2.00"))
print(f"Outcome: {decision.outcome.value}")
~~~

### 3. Web3 Native Setup (Real Transactions)

To send real transactions on Base or Ethereum, use the `EVMSigner`:

~~~python
from zerix import EVMSigner, JSONRPCProvider

# Initialize real Web3 provider and signer
provider = JSONRPCProvider(rpc_url="https://sepolia.base.org", chain_id=84532)
signer = EVMSigner(rpc_url="https://sepolia.base.org", chain_id=84532)

client = ZerixClient(policy_engine=policy, signer=signer, provider=provider)
~~~

*Read the full [Web3 Guide](docs/WEB3_GUIDE.md) for details.*

## 📊 Dashboard

Zerix comes with a built-in, zero-dependency dashboard to monitor your agents. 

~~~bash
python scripts/run_dashboard.py
~~~
Open `http://localhost:8000` to view the UI.

## 🛡️ Security Principles

1. **Non-custodial forever:** Zerix never stores private keys in a centralized server (unless self-hosted via ENV).
2. **Fail-closed:** If anything goes wrong, the transaction is DENIED.
3. **Policy lives in code, not in prompts:** Agents cannot "talk" their way out of a spending cap.

## 📄 License

Apache-2.0
