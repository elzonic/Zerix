# Zerix Roadmap

This document describes Zerix's development phases from concept to production.

**Guiding principle:** Every phase must be *shippable*.

---

## Phase 0 — Foundation (Weeks 1–4) ✅ COMPLETED

**Goal:** Prove that the *intent → policy → signer* concept works.

### Deliverables
- [x] **0.1** Python package skeleton
- [x] **0.2** `ZerixClient` with a `transfer()` method
- [x] **0.3** Policy engine v0 (spending caps + allowlist)
- [x] **0.4** Real EVM Signer integration (EIP-1559)
- [x] **0.5** `as_langchain_tools()` + OpenAI schemas

---

## Phase 1 — Public Alpha (Weeks 5–10) ✅ COMPLETED

**Goal:** Release an alpha with strict security limits.

### Deliverables
- [x] **1.1** Full policy engine (Caps, Allowlists, Time Window, Fail-closed)
- [x] **1.2** Human-in-the-loop (HITL) approval queue
- [x] **1.3** Multi-provider signer (Turnkey + Privy adapters)
- [x] **1.4** Structured audit log (JSONL)
- [x] **1.5** `as_openai_tools()` & `as_mcp_tools()`
- [x] **1.6** Web dashboard (Modern UI, read-only)

---

## Phase 2 — Beta (Weeks 11–20) ✅ COMPLETED

**Goal:** Scale to multi-chain, add automation, and enable self-hosting.

### Deliverables
- [x] **2.1** Multi-chain (EVM JSON-RPC Provider)
- [x] **2.2** Automation engine (Recurring transfers)
- [x] **2.3** x402 & MPP support (HTTP 402 automatic payments)
- [x] **2.4** Self-hosting (Docker)
- [x] **2.5** TypeScript SDK (beta)
- [x] **2.6** Webhooks & event stream
- [x] **2.7** Policy DSL (JSON loader & templates)

---

## Phase 3 — Production (Weeks 21–32) ⏳ IN PROGRESS

**Goal:** Enterprise-ready. SLA, compliance, and ecosystem.

### Deliverables
- [ ] **3.1** SLA & uptime guarantee
- [ ] **3.2** Team & role management (Multi-tenant)
- [x] **3.3** Advanced compliance (CSV Audit Export)
- [x] **3.4** Policy templates (Trading Bot, API Micropayments)
- [ ] **3.5** Plugin system
- [ ] **3.6** Performance & scale (10k+ agents)
- [ ] **3.7** Go-to-market (Enterprise docs)

---

## Phase 4 — Ecosystem (Ongoing)

- [ ] Agent-to-agent payments (x402 clearing layer)
- [ ] Policy marketplace
- [ ] Formal verification (TLA+)
- [ ] Go and Rust SDKs
- [ ] Public RFC model for governance

---

## Non-Negotiable Principles
1. **Non-custodial forever.** Zerix will never store a private key.
2. **Fail-closed.** When in doubt, deny.
3. **Policy lives in infrastructure, not in the prompt.**
4. **Open source core.** Core security features are Apache-2.0.
