# @zerix/sdk (TypeScript)

TypeScript SDK for interacting with the Zerix Python Backend.

## Installation
`npm install @zerix/sdk`

## Usage
```typescript
import { ZerixClient } from '@zerix/sdk';

const client = new ZerixClient('http://localhost:8000');
const response = await client.transfer({ to: '0x123...', amountUsd: '5.00' });
console.log(response.outcome);
