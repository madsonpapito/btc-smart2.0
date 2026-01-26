# SOP: Chain Synchronization (Layer 1)

## Goal
Fetch current balances and historical transactions for the user's wallet on Base Chain to determine "Real World" state.

## Inputs
- `WALLET_ADDRESS` (Env)
- RPC Endpoint: `https://mainnet.base.org` (or Basescan API)

## Logic
1.  **Fetch Balances**:
    - Query Aave v3 Pool Contract for 'supply' balance of WBTC and USDC.
    - Query standard ERC20 token balance for WBTC and USDC (Wallet hold).
    - **Total Balance** = Wallet Balance + Aave Supply Balance.

2.  **Fetch History (Transactions)**:
    - Use Basescan API `?module=account&action=tokentx` to get ERC20 transfers.
    - Filter for WBTC and USDC contracts.
    - Identify "Cycles": A cycle starts with a "DEPOSIT" (Buy) or "REBALANCE BUY".

## Output Shape
Returns a list of assets with their current amounts.
```json
{
  "WBTC": 0.05,
  "USDC": 1500.00,
  "last_sync_block": 12345678
}
```

## Contract Addresses (Base)
- **WBTC**: `0x...` (Need to verify)
- **USDC**: `0x...` (Need to verify)
- **Aave Pool**: `0x...` (Need to verify)
