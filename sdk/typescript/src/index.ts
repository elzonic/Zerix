/**
 * Zerix TypeScript SDK
 * 
 * This SDK connects your JS/TS AI agents to the Zerix Python backend.
 * (Assuming Zerix is running locally on port 8000 or hosted on a server).
 */

export interface TransferRequest {
    to: string;
    amountUsd: string;
}

export interface ZerixResponse {
    outcome: 'allowed' | 'denied' | 'held';
    reason: string;
}

export class ZerixClient {
    private baseUrl: string;

    constructor(baseUrl: string = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
    }

    /**
     * Executes a transfer request through the Zerix Policy Engine.
     */
    public async transfer(request: TransferRequest): Promise<ZerixResponse> {
        try {
            const response = await fetch(`${this.baseUrl}/api/transfer`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    to: request.to,
                    amount_usd: request.amountUsd,
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP Error: ${response.status}`);
            }

            const data = await response.json();
            return {
                outcome: data.outcome,
                reason: data.reason,
            };
        } catch (error) {
            // Fail-closed: If the server is unreachable, deny the transfer.
            return {
                outcome: 'denied',
                reason: `SDK Network Error (fail-closed): ${error}`,
            };
        }
    }

    /**
     * Returns OpenAI tool schema for JS/TS environments.
     */
    public getOpenAIToolSchema() {
        return {
            type: "function",
            function: {
                name: "zerix_transfer",
                description: "Transfer USDC to a recipient, subject to Zerix security policy.",
                parameters: {
                    type: "object",
                    properties: {
                        to: { type: "string", description: "The recipient address." },
                        amount_usd: { type: "string", description: "Amount in USD (e.g. '5.00')." }
                    },
                    required: ["to", "amount_usd"]
                }
            }
        };
    }
}
