# Task Plan

## Phase 1: B - Blueprint (Vision & Logic)
- [x] **Discovery**: User requirements linked: tracking, real-time comparison, Telegram alerts, Base chain.
- [x] **Data Schema**: Defined in `gemini.md`.
- [x] **Research**: Verified Basescan API & Base Chain RPC.

## Phase 2: L - Link (Connectivity)
- [x] **Basescan**: Validated (Manual Mode preferred due to Free Tier limits).
- [x] **Base RPC**: Verified for live Wallet Balances (USDC/cbBTC).
- [x] **Telegram**: Bot Connected & Verified (`test_telegram.py`).

## Phase 3: A - Architect (The 3-Layer Build)
- [x] **Tools**: `fetch_portfolio.py`, `send_alert.py`.
- [x] **State Management**: `data/state.json` tracks inputs/history.

## Phase 4: S - Stylize (Refinement & UI)
- [x] **Dashboard UI**: Dark Theme, Action Manager, Range Table (User Defined).
- [x] **Smart Logic**: Implemented Price Ranges (109k-119k = 35% BTC, etc.).
- [x] **Action Box**: "COMPRA/VENDA" box with specific amounts.

## Phase 5: T - Trigger (Deployment & Automation)
- [x] **Hold Comparison**: Added "Strategy (Smart)" vs "Strategy (HODL)" metrics.
- [x] **Alerts**: Dashboard auto-checks and sends Telegram msg on significant actionable deviation.
- [x] **Cloud Deploy**: Deployed to Streamlit Community Cloud. 
- [x] **Fixes**: 
    - [x] Price Feed (Multi-source Fallback)
    - [x] RPC (Multi-RPC Fallback for Cloud IP Limits)
    - [x] Aave Integration (Track aUSDC/acbBTC)
    - [x] Production Cleanup (Removed Debug & Test Buttons)

## Maintenance
- **Manual Input**: User must log Deposits/Trades in Dashboard Action Manager.
- **Secrets**: Ensure `WALLET_ADDRESS` and `TELEGRAM_` keys are set in Streamlit Cloud Secrets.
