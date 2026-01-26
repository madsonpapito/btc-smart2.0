# gemini.md - Project Constitution

## 1. Data Schemas

### Input Schema
#### `transaction_input` (Source: Basescan/User Input)
```json
{
  "tx_hash": "string (0x...)",
  "timestamp": "ISO8601 string",
  "type": "DEPOSIT | WITHDRAWAL | BUY | SELL | REBALANCE",
  "asset": "BTC | USDC | USD",
  "amount": "float",
  "price_at_tx": "float (optional, fetched if missing)",
  "gas_fee": "float",
  "source": "OKX Wallet | Aave | Monthly Contribution"
}
```

#### `market_data_input` (Source: Price Feed)
```json
{
  "timestamp": "ISO8601 string",
  "btc_price_usd": "float"
}
```

### Output Payload Schema
#### `dashboard_state`
```json
{
  "last_updated": "ISO8601 string",
  "portfolio": {
    "total_value_usd": "float",
    "btc_balance": "float",
    "stable_balance": "float",
    "allocation_btc_pct": "float",
    "allocation_stable_pct": "float"
  },
  "performance": {
    "smart_portfolio_pnl_usd": "float",
    "smart_portfolio_pnl_pct": "float",
    "hodl_strategy_pnl_usd": "float",
    "hodl_strategy_pnl_pct": "float"
  },
  "status": {
    "current_range_top": "float",
    "current_range_bottom": "float",
    "needs_rebalance": "boolean",
    "rebalance_action": "BUY | SELL | HOLD"
  }
}
```

#### `telegram_alert`
```json
{
  "api_token": "env.TELEGRAM_TOKEN",
  "chat_id": "env.TELEGRAM_CHAT_ID",
  "message": "string (formatted update)"
}
```

## 2. Behavioral Rules
1.  **Rebalance Trigger**: If BTC price moves ±5% from the last rebalance point (or range center), trigger an alert.
2.  **Accumulation**: Sell high, buy low logic to accumulate value/WBTC.
3.  **Benchmark**: Always calculate current portfolio value vs. value if strictly HODLed from initial inputs.
4.  **Automation**: Prefer Basescan API/RPC data over manual input. Manual input only for defining monthly deposit amounts if not inferable.
5.  **Monthly Cycles**: Track "cycles" of monthly deposits and their subsequent buy/sell actions.

## 3. Architectural Invariants
-   **Data-First**: Schema must be defined before tools are built.
-   **3-Layer Architecture**: Architecture (SOPs) -> Navigation -> Tools (scripts).
-   **Self-Healing**: Analyze -> Patch -> Test -> Update Architecture.
-   **Determinism**: Business logic must be deterministic; no probabilistic guessing in critical paths.
-   **Source of Truth**: On-chain data (Base chain) via Basescan/RPC is primary. Price feeds (CoinGecko/Chainlink) are secondary for valuation.
