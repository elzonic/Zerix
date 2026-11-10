# Zerix Web3 Guide

Starting from v0.2.0, Zerix can sign and broadcast real transactions to EVM-compatible blockchains (Ethereum, Base, Polygon, etc.).

## Prerequisites

You need an RPC URL (e.g., from Alchemy, Infura, or the public Base Sepolia RPC) and a funded wallet.

## How to send a real transaction

```python
from decimal import Decimal
from zerix import ZerixClient, PolicyEngine, SpendingCap, EVMSigner, JSONRPCProvider

# 1. Setup the RPC Provider (Base Sepolia Testnet)
rpc_url = "https://sepolia.base.org"
provider = JSONRPCProvider(rpc_url=rpc_url, chain_id=84532)

# 2. Setup the Signer (Pass your private key or let it generate one)
# WARNING: Never hardcode private keys in production. Use env variables.
signer = EVMSigner(rpc_url=rpc_url, chain_id=84532)

# 3. Setup the Policy (Max $1 per tx for testing)
policy = PolicyEngine(cap=SpendingCap(per_tx_usd=Decimal("1.00")))

# 4. Initialize ZerixClient
client = ZerixClient(
    policy_engine=policy,
    signer=signer,
    provider=provider
)

# 5. Execute the transfer
# (Assuming your wallet has Base Sepolia ETH)
decision = client.transfer(to="0xRecipientAddress...", amount_usd=Decimal("0.01"))

print(f"Status: {decision.outcome.value}")
print(f"Reason: {decision.reason}")
