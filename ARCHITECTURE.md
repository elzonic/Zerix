# Zerix Architecture

## 1. Architectural Principles

Zerix is built on one principle: **separation of authority from intelligence**.
The LLM may decide *what* it wants to do; Zerix decides *whether* that is allowed;
the signer executes *only* what has been authorized.

```
┌─────────────────────────────────────────────────────────────┐
│                      AGENT RUNTIME                          │
│  (LangChain / OpenAI Agents SDK / MCP / custom)             │
│                                                             │
│   LLM → tool call: zerix.transfer(intent)                   │
└──────────────────────────┬──────────────────────────────────┘
                           │  intent (structured JSON)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    ZERIX POLICY ENGINE                      │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ Validator   │→ │ Rule Engine │→ │ Decision            │ │
│  │ (schema)    │  │ (caps,      │  │ (ALLOW / DENY /     │ │
│  │             │  │  allowlist, │  │  HOLD_FOR_HUMAN)    │ │
│  │             │  │  time)      │  │                     │ │
│  └─────────────┘  └─────────────┘  └──────────┬──────────┘ │
│                                               │            │
│  Fail-closed: error/timeout → DENY            │            │
└───────────────────────────────────────────────┼────────────┘
                                                │ authorized intent
                                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    SIGNER ADAPTER LAYER                     │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌───────────────────────────┐  │
│  │ Turnkey  │  │  Privy   │  │ Coinbase AgentKit Wallet  │  │
│  │ (HSM)    │  │ (MPC)    │  │ Provider                  │  │
│  └──────────┘  └──────────┘  └───────────────────────────┘  │
│                                                             │
│  The private key NEVER touches the Agent Runtime.           │
└──────────────────────────┬──────────────────────────────────┘
                           │ signed tx
                           ▼
                     ┌──────────┐
                     │  CHAIN   │
                     └──────────┘
```

## 2. Core Components

### 2.1 `ZerixClient` (Python SDK)
The developer entry point. Manages API key authentication, connection to the policy engine,
and provides tool adapters for various agent frameworks.

### 2.2 Policy Engine
The most critical component. It receives an **intent** (not a finished transaction),
validates it against the active policy, and returns a decision.

**Rules that live here (not in the prompt):**
- Per-transaction cap (USD & native token)
- Daily / weekly outflow limits
- Recipient allowlist / blocklist
- Contract allowlist (only approved protocols)
- Time window (agent only active during certain hours)
- Cadence throttle (maximum frequency)
- Human-approval threshold

**Fail-closed behavior:** if the policy engine is unreachable or evaluation errors,
the default decision is **DENY**.

### 2.3 Signer Adapter Layer
An abstraction over the wallet provider. Zerix does not care whether signing is
performed by Turnkey (secure enclave), Privy (MPC), or Coinbase AgentKit. As long
as the adapter implements the `sign(intent) -> SignedTx` interface, it can be used.

### 2.4 Tool Adapter
Turns `ZerixClient` into a tool recognized by agent frameworks:
- `as_langchain_tools()`
- `as_openai_tools()`
- `as_mcp_tools()` (Model Context Protocol)

This lets an agent “install” Zerix with a single line of code or a single natural-language command.

### 2.5 Audit & Observability
Every intent — whether *allowed*, *denied*, or *held* — produces a **structured audit log**:
```json
{
  "timestamp": "2026-11-10T08:00:00Z",
  "agent_id": "trading-bot-01",
  "intent_type": "transfer",
  "amount_usd": 20,
  "recipient": "0x...",
  "decision": "ALLOW",
  "policy_id": "pol_abc123",
  "reason": "within_per_tx_and_daily_cap"
}
```
Logs can be shipped to webhooks, files, or an external observability system.

## 3. Data Flow: Transfer

1. **Agent** calls `zerix.transfer({"to": "...", "amount": 20, "asset": "USDC"})`.
2. The **SDK** converts the call into a structured *intent* (JSON) and sends it to the
   Policy Engine via API (or in-process if embedded).
3. The **Policy Engine** validates the intent against that agent's policy.
4. If **DENY** → the SDK returns a structured error to the agent (the agent can try an
   alternative step or report to the user).
5. If **HOLD** → the intent enters the HITL queue; the agent receives a “pending approval” status.
6. If **ALLOW** → the Policy Engine forwards the intent to the **Signer Adapter**.
7. The **Signer** signs the transaction (private key remains in HSM/MPC).
8. The transaction is broadcast to the chain; the hash is returned to the agent and
   recorded in the audit log.

## 4. Deployment Modes

| Mode | Best for | Policy Engine | Signer |
|---|---|---|---|
| **Cloud (SaaS)** | Individuals, small teams | Managed by Zerix | User-chosen provider |
| **Self-hosted (Docker)** | Enterprises, high-privacy | Self-operated | User-chosen provider |
| **Embedded (library-only)** | Prototypes, local agents | In-process (SQLite) | Local provider (e.g., testnet) |

## 5. Reference Technology Stack

- **Runtime:** Python 3.10+
- **Schema validation:** Pydantic
- **Policy engine:** Python (core), exposed as an API via FastAPI (optional)
- **Signers:** Turnkey / Privy / Coinbase AgentKit (via adapters)
- **Database (self-hosted):** PostgreSQL for policies and audit logs
- **Deployment:** Docker, Docker Compose, Kubernetes (Helm chart in Phase 3)
