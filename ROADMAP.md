# Zerix Roadmap

This document describes Zerix's development phases from concept to production,
along with the exit criteria for each phase.

**Guiding principle:** Every phase must be *shippable*. No phase ends without
an artifact that can be used by real users.

---

## Phase 0 — Foundation (Weeks 1–4)

**Goal:** Prove that the *intent → policy → signer* concept works end-to-end on testnet.

### Deliverables

| # | Item | Definition of Done |
|---|---|---|
| 0.1 | Python package skeleton + PyPI publish | `pip install zerix` succeeds in a clean environment |
| 0.2 | `ZerixClient` with a `transfer()` method | Can send USDC on Base Sepolia via a mock provider |
| 0.3 | Policy engine v0 (spending caps + allowlist) | Unit test: transaction above cap → `Denied` |
| 0.4 | One signer integration (Turnkey **or** Privy) | Transaction signed & confirmed on testnet |
| 0.5 | `as_langchain_tools()` + example agent | A LangChain agent can call `zerix.transfer` |

### Exit criteria
- [ ] 3 external users (beta testers) successfully perform a testnet transfer via an agent.
- [ ] Quickstart documentation is complete and tested by someone outside the team.

---

## Phase 1 — Public Alpha (Weeks 5–10)

**Goal:** Release an alpha that can be used on mainnet with strict limits.

### Deliverables

| # | Item | Definition of Done |
|---|---|---|
| 1.1 | Full policy engine | Supports: per-tx cap, daily cap, weekly cap, recipient allowlist, contract allowlist, time window, **fail-closed** |
| 1.2 | Human-in-the-loop (HITL) | Transactions above `require_human_above_usd` enter an approval queue (API + webhook) |
| 1.3 | Multi-provider signer | Turnkey + Privy + Coinbase AgentKit adapters |
| 1.4 | Structured audit log | Every decision (`allowed`/`denied`/`held`) is recorded with a reason |
| 1.5 | `as_openai_tools()` & `as_mcp_tools()` | Integration with OpenAI Agents SDK and MCP |
| 1.6 | Web dashboard (read-only) | View policies, transactions, and HITL status |

### Exit criteria
- [ ] 50+ agents on Base mainnet with total volume < $10,000 (intentionally limited).
- [ ] No fund-loss incidents caused by policy bypass.
- [ ] Internal security review complete (see `SECURITY.md`).

---

## Phase 2 — Beta (Weeks 11–20)

**Goal:** Scale to multi-chain, add automation, and enable self-hosting.

### Deliverables

| # | Item | Definition of Done |
|---|---|---|
| 2.1 | Multi-chain | Base, Ethereum, Solana (via provider adapters) |
| 2.2 | Automation engine | DCA, conditional orders (“sell if down 10%”), recurring transfers |
| 2.3 | x402 & MPP support | Agents can pay for APIs/data over HTTP 402 |
| 2.4 | Self-hosting (Docker) | `docker compose up` runs Zerix end-to-end with policy engine & DB |
| 2.5 | TypeScript SDK (beta) | `npm install @zerix/sdk` with feature parity to Python core |
| 2.6 | Webhooks & event stream | Real-time notifications for transactions, denials, and HITL |
| 2.7 | Policy DSL | Policies can be expressed as YAML/JSON and loaded from files |

### Exit criteria
- [ ] 500+ active agents; monthly volume > $100,000.
- [ ] External security audit (at least one firm) complete; zero critical findings.
- [ ] Self-hosting documentation tested on fresh VPS by 3 independent users.

---

## Phase 3 — Production & General Availability (Weeks 21–32)

**Goal:** Enterprise-ready. SLA, compliance, and ecosystem.

### Deliverables

| # | Item | Definition of Done |
|---|---|---|
| 3.1 | SLA & uptime guarantee | 99.9% uptime for the policy engine API; public status page |
| 3.2 | Team & role management | Multi-tenant: organizations, members, roles (admin/approver/viewer) |
| 3.3 | Advanced compliance | Audit log export (CSV/JSON), retention policies, 1-year+ retention |
| 3.4 | Policy templates | Ready-made templates: “Trading Bot Safe”, “Treasury Conservative”, “API Micropayments” |
| 3.5 | Plugin system | Third-party providers & tools can be registered without forking |
| 3.6 | Performance & scale | Policy evaluation < 50ms p95; 10,000+ agents per instance |
| 3.7 | Go-to-market | Enterprise documentation, integration examples, and a partner program |

### Exit criteria
- [ ] 5+ enterprises using Zerix in production.
- [ ] Zero critical security incidents in the last 90 days.
- [ ] OpenSSF Best Practices Badge (passing).

---

## Phase 4 — Ecosystem & Sustainability (Ongoing)

- **Agent-to-agent payments** — Zerix as a *clearing layer* for inter-agent payments via x402/MPP.
- **Policy marketplace** — The community can share/sell battle-tested policy templates.
- **Formal verification** — Mathematical verification of the core policy engine (e.g., using TLA+).
- **Additional languages** — Go and Rust SDKs.
- **Governance** — Move to a public RFC model for major architectural decisions.

---

## Non-Negotiable Principles

1. **Non-custodial forever.** Zerix will never store a private key.
2. **Fail-closed.** When in doubt, deny.
3. **Policy lives in infrastructure, not in the prompt.** Prompts can be persuaded; code cannot.
4. **Open source core.** Core security features are always Apache-2.0.
