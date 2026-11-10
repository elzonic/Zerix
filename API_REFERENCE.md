# API Reference

## `ZerixClient`

### `__init__(api_key=None, base_url=None, agent_id=None)`
Creates a client. If `api_key` is not provided, it reads `ZERIX_API_KEY` from the environment.

### `set_policy(agent_id, policy: Policy) -> Policy`
Sets the policy for an agent. Returns the stored policy.

### `transfer(intent: TransferIntent) -> TransactionResult`
Sends a transfer intent. `TransactionResult` includes `status` (`allowed` / `denied` / `held`),
`tx_hash` (when allowed), and `reason`.

### `swap(intent: SwapIntent) -> TransactionResult`

### `get_balance(asset=None) -> Balance`

### `list_transactions(limit=50, status=None) -> list[Transaction]`

## Policy (Pydantic Model)

| Field | Type | Description |
|---|---|---|
| `max_per_tx_usd` | `float` | Per-transaction limit |
| `max_daily_usd` | `float` | Daily limit |
| `max_weekly_usd` | `float` | Weekly limit |
| `allowed_chains` | `list[str]` | Permitted chains |
| `allowed_contracts` | `list[str]` | Contract allowlist |
| `allowed_recipients` | `list[str]` | Recipient allowlist |
| `require_human_above_usd` | `float` | HITL threshold |
| `time_window` | `tuple[str, str]` | Active hours (UTC) |
| `fail_closed` | `bool` | Defaults to `True` |

## Error Classes

- `ZerixError` — base
- `PolicyDeniedError`
- `PolicyHoldError`
- `SignerError`
- `InsufficientFundsError`
- `LimitExceededError`

## MCP Tools

When running as an MCP server, Zerix exposes the tools:
`zerix.transfer`, `zerix.swap`, `zerix.get_balance`, `zerix.list_transactions`.
