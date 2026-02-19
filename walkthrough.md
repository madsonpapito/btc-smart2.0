# ⚡ BTC Smart Portfolio (B.L.A.S.T. Protocol) - Final Walkthrough

## 1. Project Overview
A semi-automated dashboard for tracking and rebalancing a Bitcoin portfolio on the Base Layer 2 Network.
- **Goal**: Accumulate BTC using volatility ranges vs a simple HODL strategy.
- **Tech**: Streamlit (Python), Web3.py (Base Chain), Telegram Bot API.
- **Protocol**: B.L.A.S.T. (Blueprint, Link, Architect, Stylize, Trigger).

## 2. Key Features

### 📊 Dashboard
- **Real-Time Data**: Fetches balances directly from Base Mainnet RPC.
- **Asset Support**: 
  - **Wallet**: USDC, USDbC (Bridged), cbBTC.
  - **Aave V3**: aUSDC (Supplied), acbBTC (Supplied).
- **Smart Allocation Logic**:
  - defined prices ranges (e.g., ~$109k-%119k → 35% BTC).
  - **Dynamic "Action Box"**: Calculates exact buy/sell amounts to stay in target.
- **Performance Comparison**:
  - Tracks **Smart Strategy Value** vs **HODL Value** (Simulated if you never traded).

### 🤖 Automation
- **Telegram Alerts**: Sends a message to your phone if the Portfolio deviates >$50 from target.
- **Resilient Connectivity**: 
  - **Price**: Coinbase -> Binance -> CoinGecko fallback.
  - **RPC**: LlamaNodes -> BlastAPI -> Base -> 1RPC fallback (Bypasses Cloud Blocks).

## 3. Architecture
- **`dashboard.py`**: Main UI and Logic Kernel.
- **`data/state.json`**: Persistence layer for "Cycles" (Trades).
- **`tools/`**:
  - `fetch_portfolio.py`: Reads Blockchain State (Wallet + Aave).
  - `send_alert.py`: Handles Telegram notifications.
  - `get_btc_price.py`: Multi-source Price Oracle.

## 4. Usage Guide
1.  **Deposits**: Send USDC/BTC to your Base Wallet or Supply to Aave.
2.  **Check**: Open Dashboard. It auto-updates your "Current Allocation".
3.  **Action**:
    - If "COMPRA" box appears: Swap USDC -> cbBTC on Uniswap/Aerodrome.
    - **Log it**: Click `BUY BTC` in the Dashboard Action Manager to update the History.
4.  **Sleep**: The Strategy handles the math.

## 5. Deployment
- **Host**: Streamlit Community Cloud.
- **Repository**: `madsonpapito/btc-smart2.0`.
- **Status**: ✅ Deployed & Verified.
