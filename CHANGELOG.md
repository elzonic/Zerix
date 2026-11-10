# Changelog

All notable changes to this project will be documented in this file.

## [0.5.0] - 2023-11-01
### Added
- Full SaaS Dashboard UI with modern dark mode (Vercel/Apple style).
- Interactive HITL (Approve/Reject) directly from the dashboard.
- SQLite Database integration for user management.
- API Key Authentication (`POST /api/register` and protected `/api/audit`).
- Registration/Login UI for seamless onboarding.
- Profile & Logout features in Dashboard.
- Real-time full-stack integration (Python Backend -> API -> Frontend JS).

## [0.4.0] - 2023-10-27
### Added
- Published to PyPI (pip install zerix).
- Modern zero-dependency web dashboard.

## [0.3.0] - 2023-10-27
### Added
- x402 Micropayments handler (HTTP 402 auto-payments).
- Enterprise Signers: `TurnkeySigner` and `PrivySigner` adapters.
- TypeScript SDK (`@zerix/sdk`) for JS/TS agents.
- Docker setup for self-hosting.
