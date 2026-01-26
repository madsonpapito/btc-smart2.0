# SOP: Portfolio Calculation (Layer 1)

## Goal
Calculate the current value of the "Smart Portfolio" vs a benchmark "HODL Strategy" and determine if rebalancing is required.

## Inputs
- `current_holdings`: Output from `sop_chain_sync`.
- `market_data`: Current BTC price.
- `portfolio_rules`: Range definition (e.g., Min/Max price) and Target Allocation (50/50 etc).

## Logic
1.  **Valuations**:
    - `Smart Value` = (WBTC_Qty * Price) + USDC_Qty
    - `HODL Value` = Sum of all initial investments converted to BTC at entry time * Current Price (This requires accurate history tracking).
      - *Simplification*: `HODL Value` = (Total USD Invested) / (Avg Entry Price) * Current Price.

2.  **Rebalance Check**:
    - Calculate Current Weights: `BTC %` = (WBTC Value / Total Value).
    - Compare to Target Weight (e.g., 50%).
    - If deviation > 5% (User Trigger), flag `needs_rebalance = True`.

3.  **Range Check**:
    - If Price < Range Bottom or Price > Range Top, update strategy (Accumulate vs Sell).

## Output Shape
```json
{
  "smart_value": 10500.00,
  "hodl_value": 10200.00,
  "delta": 300.00,
  "btc_percentage": 56.5,
  "action": "SELL 6.5% BTC"
}
```
