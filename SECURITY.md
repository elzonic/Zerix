# Security Policy

## 1. Zerix Security Principles

Zerix is designed under the assumption that **the agent runtime is an untrusted environment**.
LLMs can be affected by prompt injection, hallucination, or exploited through the content
they read. Therefore, financial decisions **must not** depend on the prompt.

### Three pillars:

1. **The private key never lives in the agent runtime.**
   Signing is performed by an external HSM/MPC/enclave. If the agent is compromised,
   the attacker does not obtain the key.

2. **Policy is enforced in code, not in the prompt.**
   Spending caps, allowlists, and other limits live in the Policy Engine — not as
   instructions in a system prompt.

3. **Fail-closed.**
   When in doubt, on error, or on timeout → the transaction is denied.

## 2. Threat Model (Summary)

| Threat | Vector | Zerix Mitigation |
|---|---|---|
| **Prompt injection** | Malicious content from web/tool return persuades the agent to send funds to an attacker | The policy engine validates the *intent* independently; prompt injection cannot change code rules |
| **Key exfiltration** | Agent runtime compromised | No private key in runtime; signing handled by HSM/MPC |
| **Unlimited drain** | Bug loops or agent “hallucinations” cause repeated sends | Per-tx cap, daily cap, cadence throttle, circuit breaker |
| **Malicious recipient** | Agent persuaded to send to an attacker's address | Recipient allowlist/blocklist |
| **Malicious contract** | Agent interacts with a malicious contract | Contract allowlist (audited protocols only) |
| **Policy bypass** | Attacker attempts to manipulate policy evaluation | Policy validation happens outside the prompt context; two-gate control (evaluation + authorization are separate) |
| **Supply chain** | Malicious dependencies in the SDK | Dependency pinning, SBOM, automated review |

## 3. Implementation Security Posture

- **Split read vs execution:** The agent that reads data need not be the same agent
  authorized to sign.
- **Hot/cold wallet pattern:** The agent only gets access to a hot wallet with small caps;
  the cold wallet is under a separate policy.
- **Structured audit log** for every decision (allow/deny/hold) — supports forensics.
- **Webhooks & alerting** for anomalies (denial spikes, large-transfer attempts).

## 4. Vulnerability Reporting

**DO NOT open a public issue for security vulnerabilities.**

Send reports to: **security@zerix.dev** (PGP key available at
[`/.well-known/security.txt`](/.well-known/security.txt)).

We will:
1. Acknowledge receipt within **48 hours**.
2. Provide an initial assessment within **5 business days**.
3. Target a patch for critical vulnerabilities within **14 days**.

We will not take legal action against good-faith security research.

## 5. Dependency & Supply Chain

- All dependencies are pinned with hashes.
- An SBOM (Software Bill of Materials) is published with every release.
- CI runs `pip-audit` and automated review for PRs that change dependencies.
- Core security code (policy engine) has at least 90% test coverage.

## 6. Audits

| Phase | Audit | Status |
|---|---|---|
| Alpha | Internal security review | Target: Phase 1 |
| Beta | External audit (independent firm) | Target: Phase 2 |
| Production | Continuous auditing + bug bounty | Target: Phase 3 |
