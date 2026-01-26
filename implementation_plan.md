# [Aave Portfolio Integration]

The user's funds are supplied to Aave V3 on Base, not held as liquid tokens. We need to track `aTokens` (receipt tokens) to correctly calculate the portfolio value.

## User Review Required
> [!NOTE]
> This change will sum your **Liquid Wallet Balance** + **Aave Supplied Balance**. It treats supplied assets as "part of the portfolio" for rebalancing calculations.

## Proposed Changes

### Tools Layer
#### [MODIFY] [fetch_portfolio.py](file:///c:/BTC%20-%20SMART%20PORFOLIO/tools/fetch_portfolio.py)
- Add `aUSDC` and `acbBTC` to the `TOKENS` dictionary with their Base V3 addresses.
- The script will automatically fetch their balances (since they are ERC20s).

### Dashboard Layer
#### [MODIFY] [dashboard.py](file:///c:/BTC%20-%20SMART%20PORFOLIO/dashboard.py)
- Update the summation logic:
  - `Total BTC` = `cbBTC` + `WBTC` + `acbBTC`
  - `Total USD` = `USDC` + `USDbC` + `aUSDC`

## Verification Plan

### Automated Tests
- None (Blockchain interaction requires live keys).

### Manual Verification
1.  **Deploy**: Push changes to GitHub.
2.  **User Action**: Refresh Streamlit Cloud.
3.  **Success Criteria**:
    - Dashboard shows Total Portfolio ~$99.95 (matches user print).
    - `Current Allocation` pie chart updates from 0%.
