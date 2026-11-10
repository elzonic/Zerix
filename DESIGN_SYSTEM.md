# Zerix Design System

Design system for the **Zerix web dashboard** (policy management, audit log, HITL queue).
Focus: clarity of financial information, security status, and critical actions.

## 1. Design Principles

1. **Calm surfaces, decisive accents.** Most of the UI is a neutral canvas;
   accent colors appear only for status and critical actions.
2. **Money is data.** Amounts, addresses, and hashes use monospace.
3. **Security is visible.** Policy status (active/denied/held) is always visible,
   not hidden behind a menu.

## 2. Color Tokens

| Token | Value | Usage |
|---|---|---|
| `--zx-bg` | `#F7F8FA` | Main background |
| `--zx-surface` | `#FFFFFF` | Cards, panels |
| `--zx-ink` | `#1A1D23` | Primary text |
| `--zx-ink-muted` | `#6B7280` | Secondary text |
| `--zx-primary` | `#2563EB` | Primary accent, CTA |
| `--zx-success` | `#059669` | Status ALLOW / confirmed |
| `--zx-warning` | `#D97706` | Status HOLD / pending |
| `--zx-danger` | `#DC2626` | Status DENY / failed |
| `--zx-mono-bg` | `#F3F4F6` | Background for addresses/hashes |

**Color principle:** security status (allow/hold/deny) uses consistent semantic colors
across the entire application.

## 3. Typography

| Role | Font | Size |
|---|---|---|
| UI / body | Inter | 14px base |
| Headings | Inter (600) | 20–28px |
| **Address, amount, hash** | **JetBrains Mono** | 13px |
| Caption | Inter | 12px |

Why monospace for addresses: prevents misreading similar-looking characters
(`0xABC` vs `0xAB0`) — a common pattern in wallets and explorers.

## 4. Spacing & Radius

- **Spacing scale:** 4px base (`4, 8, 12, 16, 24, 32, 48`).
- **Radius:** `sm=4px`, `md=8px`, `lg=12px`, `full=9999px`.
- Cards and panels use `md`; buttons and badges use `full`.

## 5. Core Components

### 5.1 Policy Card
Shows the active policy for a single agent:
- Policy name & agent ID
- Per-tx / daily cap (in USD)
- Allowlist counts (contract/recipient)
- Status: `Active` / `Paused` / `Draft`
- Actions: Edit, Pause, Duplicate

### 5.2 Transaction Row
Each audit log row:
- Timestamp (monospace)
- Agent ID
- Intent type (`transfer` / `swap` / `approve`)
- Amount (monospace, with asset symbol)
- Recipient (address pill, copyable)
- **Decision badge:** `ALLOW` (green), `HOLD` (yellow), `DENY` (red)
- Reason (tooltip)

### 5.3 HITL Queue Item
Human approval queue:
- Intent summary in human-readable language (“Send 150 USDC to 0x... on Base”)
- The policy that was violated
- Buttons: **Approve** / **Deny** / **Approve with modified cap**
- Countdown expiry (if applicable)

### 5.4 Address Pill
Component to display an address:
```
0x1234…abcd  [copy]
```
Uses monospace with a copy button. Supports ENS/name resolution when available.

## 6. Accessibility

- Minimum contrast of WCAG AA (4.5:1 for normal text).
- Status never relies on color alone — a text label is always present (`ALLOW`, `DENY`, `HOLD`).
- All components are keyboard-operable.

## 7. Implementation

This design system is distributed as:
- **Figma library** (public)
- **React component library** (`@zerix/ui`) — Phase 2
- **Design tokens** in JSON format (`tokens.json`) so they can be consumed
  by Tailwind, CSS variables, or any other framework.
