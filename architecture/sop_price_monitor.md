# SOP: Price Monitor & Alerting (Layer 1)

## Goal
Fetch real-time BTC prices and send formatted notifications to Telegram.

## Inputs
- `coingecko_id`: `bitcoin`
- `telegram_config`: Token/ChatID

## Logic
1.  **Fetch Price**:
    - URL: `https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd`
    - Fallback: Coinbase API.

2.  **Notification Formatter**:
    - **Header**: Emojis based on movement (🚀 Up, 🔻 Down, ⚖️ Rebalance).
    - **Body**: Current Price, Portfolio Value, Comparison (Smart vs HODL).
    - **Action**: "Rebalance Needed: Sell 0.01 BTC" or "Range Stable".

## Output Shape
- Boolean success.
- Side effect: Telegram Message sent.
