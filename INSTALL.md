# Installing Zerix

## 1. Quick Install (Python SDK)

```bash
pip install zerix
```

Requires Python 3.10+.

## 2. Environment Configuration

Zerix reads configuration from environment variables:

```bash
export ZERIX_API_KEY="zx_live_xxxxxxxxxxxxxxxx"
export ZERIX_BASE_URL="https://api.zerix.dev"   # optional, for self-hosted
```

For agents running in CI/CD or containers, inject the API key via a secret
manager (never hardcode it in code).

## 3. Installing for Agent Frameworks

### 3.1 LangChain

```bash
pip install zerix coinbase-agentkit-langchain langchain-openai
```

```python
from zerix.tools import as_langchain_tools
tools = as_langchain_tools(client, agent_id="my-agent")
```

### 3.2 OpenAI Agents SDK

```bash
pip install zerix openai-agents
```

```python
from zerix.tools import as_openai_tools
tools = as_openai_tools(client, agent_id="my-agent")
```

### 3.3 MCP (Model Context Protocol)

Run Zerix as an MCP server:

```bash
zerix mcp-server --api-key $ZERIX_API_KEY
```

Then instruct your agent:

> *“Use the `zerix` MCP server for all wallet operations. The policy is already configured on the server.”*

This pattern lets the agent “install” Zerix without any code changes —
just by adding the MCP server to the agent's configuration.

## 4. Self-Hosting (Docker)

```bash
git clone https://github.com/zerix-dev/zerix.git
cd zerix
cp .env.example .env
# fill in ZERIX_DB_URL, ZERIX_SIGNER_PROVIDER, etc.
docker compose up -d
```

This runs:
- Policy Engine API (`:8080`)
- PostgreSQL (`:5432`)
- Web dashboard (`:3000`)

Verify:

```bash
curl http://localhost:8080/health
# {"status":"ok","version":"0.x.x"}
```

## 5. Verifying the Installation

```python
import zerix
client = zerix.ZerixClient()
print(client.health())   # {'status': 'ok'}
print(client.me())       # agent info & active policy
```
