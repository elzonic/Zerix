# Zerix

**Policy-enforcing wallet middleware for AI agents.**

Zerix gives your AI agent access to an on-chain wallet — without ever exposing the private key.
The agent sends an *intent* (a structured request), Zerix validates it against the policies you
define, then forwards it to the wallet provider for signing.

[![PyPI](https://img.shields.io/pypi/v/zerix)](https://pypi.org/project/zerix/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Security Policy](https://img.shields.io/badge/security-policy-blue)](SECURITY.md)

---

## Why Zerix?

An agent wallet without guardrails is an accident waiting to happen. Prompt injection,
hallucination, or an accidental loop can drain funds in seconds. Zerix separates
**intelligence** (the LLM) from **authority** (signing) through a single policy layer
that cannot be bypassed by a prompt.

- **Non-custodial** — The private key never touches the agent runtime.
- **Fail-closed** — If the policy engine is unavailable, the transaction is denied.
- **Provider-agnostic** — Works with Turnkey, Privy, Coinbase AgentKit, or a custom signer.
- **Python-native** — `pip install zerix`, set the API key, and use it from any agent framework.

---

## Installation

```bash
pip install zerix
```

Verify:

```python
import zerix
print(zerix.__version__)
```

Requires **Python 3.10+**.

---

## Quickstart (3 minutes)

### 1. Get an API key

Sign up at [dashboard.zerix.dev](https://dashboard.zerix.dev) (or self-host), then create an API key:

```bash
export ZERIX_API_KEY="zx_live_xxxxxxxxxxxxxxxx"
```

### 2. Define a policy

```python
from zerix import ZerixClient, Policy

client = ZerixClient(api_key="zx_live_xxx")

policy = Policy(
    max_per_tx_usd=50,
    max_daily_usd=200,
    allowed_chains=["base", "ethereum"],
    allowed_contracts=[
        "0xUniswapRouter...",
        "0xAavePool...",
    ],
    require_human_above_usd=100,
)

client.set_policy(agent_id="my-trading-agent", policy=policy)
```

### 3. Connect your agent

**Framework-agnostic** — expose Zerix as a tool:

```python
from zerix.tools import as_langchain_tools   # or as_openai_tools, as_mcp_tools

tools = as_langchain_tools(client, agent_id="my-trading-agent")

# The agent can now call: zerix.transfer, zerix.swap, zerix.get_balance
```

**Or via MCP** (Model Context Protocol) — one instruction is all the agent needs:

> *“Install Zerix and use it as your wallet tool. The API key is in the environment.”*

---

## How Agents Use Zerix

The agent **never** holds a private key. The flow is:

```
Agent (LLM) → zerix.transfer(intent) → Policy Engine → Signer (Turnkey/Privy) → Chain
                                            ↓
                                    Approve / Deny / Hold-for-human
```

Example conversation:

> **User:** “Send 20 USDC to alice.base.eth.”
>
> **Agent:** *(calls `zerix.transfer`)*
>
> **Zerix:** ✅ Approved — 20 USDC < 50 USD/tx cap, `alice.base.eth` is on the allowlist.

If the amount exceeds the cap:

> **Zerix:** ⏸️ Held — 150 USDC exceeds `max_per_tx_usd=50`. Awaiting human approval.

---

## Documentation

| Document | Contents |
|---|---|
| [`INSTALL.md`](INSTALL.md) | Detailed installation, environment configuration, self-hosting |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | System architecture, data flow, components |
| [`SECURITY.md`](SECURITY.md) | Threat model, vulnerability reporting, security posture |
| [`ROADMAP.md`](ROADMAP.md) | Development plan from alpha to production |
| [`DESIGN_SYSTEM.md`](DESIGN_SYSTEM.md) | Tokens & UI components for the dashboard |
| [`API_REFERENCE.md`](API_REFERENCE.md) | Python API & MCP tools reference |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to contribute, branch model, commit convention |

---

## License

Apache License 2.0 — see [`LICENSE`](LICENSE).
