# Zerix Architecture

Zerix is designed as a **middleware** layer. It sits between your AI agent and the blockchain, ensuring that the agent's intentions are validated by a strict policy engine before any transaction is signed.

## Core Components

1. **ZerixClient**
   The main entry point. It orchestrates the flow: Policy Check -> Signer Execution -> Audit Logging.

2. **Policy Engine**
   Evaluates transactions against rules:
   - `SpendingCap` (per-tx, daily, weekly).
   - `Allowlist` (recipient and contract addresses).
   - `TimeWindow` (restricts transactions to certain hours).
   - `HITL` (Holds transactions above a threshold for human approval).
   - *Principle: Fail-Closed (any error means DENIED).*

3. **Signers**
   Responsible for holding keys and signing transactions. The agent never touches the private keys.
   - `MockSigner`: For local testing.
   - `EVMSigner`: Native EIP-1559 signing for Web3.
   - `TurnkeySigner` / `PrivySigner`: Enterprise custody adapters.

4. **Providers**
   Responsible for reading on-chain state.
   - `JSONRPCProvider`: Connects to Base, Ethereum, or any EVM RPC.

5. **Audit Logger**
   Records every decision (allowed, denied, held) into `audit.jsonl` with the reason.

6. **x402 Handler**
   Intercepts HTTP 402 Payment Required responses from APIs and automatically pays for them using the `ZerixClient`.

## Data Flow Diagram

```text
[ AI Agent ] 
     | (calls transfer)
     v
[ ZerixClient ] ---> [ Policy Engine ] ---> (DENIED / HELD / ALLOWED)
     |
     | (if ALLOWED)
     v
[ Signer (EVM/Turnkey) ] ---> [ JSON-RPC Node ] ---> [ Blockchain ]
     |
     v
[ Audit Logger ]
