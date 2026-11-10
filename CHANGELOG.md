# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - 2023-10-27
### Added
- x402 Micropayments handler (HTTP 402 auto-payments).
- Enterprise Signers: `TurnkeySigner` and `PrivySigner` adapters.
- TypeScript SDK (`@zerix/sdk`) for JS/TS agents.
- Docker setup for self-hosting.

## [0.2.0] - 2023-10-26
### Added
- Real Web3 Integration: `EVMSigner` (EIP-1559) and `JSONRPCProvider`.
- Modern Dashboard UI (Dark mode, zero-dependency).
- Policy Templates (`trading_bot_safe`, `api_micropayments`).
- Webhooks and Recurring Transfer engine.
- CSV Audit Export for compliance.

## [0.1.0] - 2023-10-25
### Added
- Initial alpha release.
- Fail-closed Policy Engine (Spending caps, allowlists).
- HITL (Human-in-the-Loop) thresholds.
- MockSigner and Audit Logging.
- LangChain, OpenAI, and MCP tool schemas.
- Basic read-only dashboard.
