import streamlit as st
import pandas as pd
import json
import os
import time
from datetime import datetime
from tools.get_btc_price import get_btc_price
from tools.fetch_portfolio import fetch_portfolio

# Page Config
st.set_page_config(page_title="BTC Smart Portfolio", page_icon="⚡", layout="wide")

# Paths
STATE_FILE = "data/state.json"

# Load State
def load_state():
    if not os.path.exists(STATE_FILE):
        return {
            "last_check_price": 0,
            "target_allocation_btc": 0.5,
            "range_top": 100000,
            "range_bottom": 50000,
            "deposits": []  # List of {date, type, amount_usd, amount_btc, price, profit}
        }
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

state = load_state()
load_css()

# --- HEADER ---
st.markdown("""
    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;'>
        <h1 style='margin: 0; color: #FAFAFA;'><span style='color: #00E5FF;'>⚡ SMART</span> BTC PORTFOLIO</h1>
        <div style='text-align: right;'>
            <span style='color: #8899A6; font-size: 0.9rem;'>STATUS DA REDE</span><br>
            <span style='color: #00FFA3; font-weight: bold;'>● ONLINE (BASE)</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- GLOBAL DATA FETCH ---
price = get_btc_price()
if not price:
    st.error("Failed to fetch BTC Price")
    st.stop()

# Fetch Wallet Balances
with st.spinner("Syncing Chain Data..."):
    portfolio_data = fetch_portfolio()

# Calculate Holdings
wallet_btc = 0.0
wallet_usdc = 0.0
if portfolio_data:
    # SUM Native + Aave Supplied BTC
    wallet_btc = portfolio_data["wallet"].get("cbBTC", 0) + portfolio_data["wallet"].get("WBTC", 0) + portfolio_data["wallet"].get("acbBTC", 0)
    
    # SUM Native + Bridged + Aave Supplied USD
    wallet_usdc = portfolio_data["wallet"].get("USDC", 0) + portfolio_data["wallet"].get("USDbC", 0) + portfolio_data["wallet"].get("aUSDC", 0)
else:
    st.error("⚠️ Falha na Conexão RPC (Blockchain).")
    st.warning("""
    **Possíveis Causas:**
    1. (Cloud) Você esqueceu de configurar os **Secrets**? (WALLET_ADDRESS).
    2. (Cloud) O RPC Público da Base pode estar bloqueando o IP.
    
    *O painel está usando valores zerados/padrão.*
    """)

# ... (omitted lines) ...

# --- DEBUG FOOTER ---
with st.expander("🛠️ Debug Information (Cloud Diagnostics)"):
    st.write("If you see $0.00 above, check these values:")
    
    # Check Env Var
    env_wallet = os.getenv("WALLET_ADDRESS")
    if env_wallet:
        # Show exact representation to catch quotes/newlines/spaces (e.g. '0x...' vs "0x...")
        st.success(f"Locked Wallet (repr): `{repr(env_wallet)}`")
        
        # LINK TO BASESCAN
        st.markdown(f"🔎 [**Clique aqui para ver seus Fundos na Basescan**](https://basescan.org/address/{env_wallet})", unsafe_allow_html=True)

# Aave Data
aave_collat = portfolio_data["aave"].get("total_collateral_usd", 0)
aave_debt = portfolio_data["aave"].get("total_debt_usd", 0)

# FIX: Do not add aave_collat again. wallet_usdc/btc already include aTokens.
total_usdc_equiv = wallet_usdc 
total_btc_val = wallet_btc * price
total_portfolio_val = total_usdc_equiv + total_btc_val
current_alloc_pct = (total_btc_val / total_portfolio_val * 100) if total_portfolio_val > 0 else 0

# --- LAYOUT GRID ---
# Top Metrics Bar
m1, m2, m3, m4 = st.columns(4)
m1.metric("BTC Price", f"${price:,.2f}")
m2.metric("Total Portfolio", f"${total_portfolio_val:,.2f}")
m3.metric("Current Allocation", f"{current_alloc_pct:.1f}% BTC")
m4.metric("Cycle Count", f"{len(state['deposits'])}")

st.markdown("---")

# Main Split: Left (Inputs/Logic) - Right (History)
col_left, col_right = st.columns([1.5, 1])

with col_left:
    # 1. INPUTS / ACTION
    st.subheader("📝 Action Manager", help="Registre aqui seus Depósitos e Trades manualmente para manter o Histórico de Ciclos atualizado. O Saldo Atual é sincronizado automaticamente.")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        qty_btc = c1.number_input("BTC Amount", min_value=0.0, format="%.6f")
        qty_usdc = c2.number_input("USDC Amount", min_value=0.0, format="%.2f")
        
        b1, b2, b3 = st.columns(3)
        if b1.button("📥 DEPOSIT (New)", use_container_width=True):
            new_tx = {
                "cycle": len(state["deposits"]) + 1,
                "type": "DEPOSIT",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "btc_amount": qty_btc,
                "usd_amount": qty_usdc,
                "price": price,
                "total_val": (qty_btc * price) + qty_usdc,
                "profit": 0 # NA for deposit
            }
            state["deposits"].append(new_tx)
            save_state(state)
            st.rerun()
            
        if b2.button("📈 BUY BTC", use_container_width=True):
            new_tx = {
                "cycle": len(state["deposits"]) + 1,
                "type": "BUY",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "btc_amount": qty_btc,
                "usd_amount": qty_usdc, # Cost
                "price": price,
                "total_val": total_portfolio_val, # Snapshot
                "profit": 0 # Calc PnL later
            }
            state["deposits"].append(new_tx)
            save_state(state)
            st.rerun()

        if b3.button("📉 SELL BTC", use_container_width=True):
             new_tx = {
                "cycle": len(state["deposits"]) + 1,
                "type": "SELL",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "btc_amount": qty_btc,
                "usd_amount": qty_usdc, # Proceeds
                "price": price,
                "total_val": total_portfolio_val,
                "profit": 0
            }
             state["deposits"].append(new_tx)
             state["deposits"].append(new_tx)
             save_state(state)
             st.rerun()

    # 2. PORTFOLIO COMPARISON
    st.markdown("### ⚖️ Portfolio Logic")
    p_col1, p_col2 = st.columns(2)
    
    with p_col1:
        st.info("**Current Allocation**")
        st.write(f"**BTC**: ${total_btc_val:,.0f} ({current_alloc_pct:.1f}%)")
        st.write(f"**USD**: ${total_usdc_equiv:,.0f} ({100-current_alloc_pct:.1f}%)")
        st.write(f"**Total**: ${total_portfolio_val:,.0f}")
        
    with p_col2:
        st.warning("**Target Allocation**")
        target_pct = state.get("target_allocation_btc", 0.5) * 100
        target_btc_val = total_portfolio_val * (target_pct/100)
        target_usd_val = total_portfolio_val * ((100-target_pct)/100)
        
        st.write(f"**BTC**: ${target_btc_val:,.0f} ({target_pct:.1f}%)")
        st.write(f"**USD**: ${target_usd_val:,.0f} ({100-target_pct:.1f}%)")
        
        # Deviation
        diff_btc = target_btc_val - total_btc_val
        if abs(diff_btc) > 10: # Noise filter
            action = "BUY" if diff_btc > 0 else "SELL"
            st.markdown(f"**Diff**: {action} ${abs(diff_btc):,.0f} BTC")

    # 3. RANGE TABLE (User Defined)
    st.markdown("### 🎯 Smart Allocation Logic")
    
    # Range Definition (Price Min, Price Max, Target Allocation %)
    # Descending order for table display
    smart_ranges = [
        (140000, float("inf"), 0.20),
        (130000, 139999, 0.25),
        (120000, 129999, 0.30),
        (109000, 119999, 0.35),
        (99000, 108999, 0.45),
        (89000, 98999, 0.55),
        (79000, 88999, 0.65),
        (69000, 78999, 0.75),
        (59000, 68999, 0.80),
        (0, 58999, 0.85) # Implied catch-all
    ]
    
    range_data = []
    target_alloc_now = 0.5 # Default
    
    for r_min, r_max, r_target in smart_ranges:
        # Check active
        is_active = False
        if r_max == float("inf"):
             if price >= r_min: is_active = True
             range_label = f"≥ ${r_min:,.0f}"
        else:
             if r_min <= price <= r_max: is_active = True
             range_label = f"${r_min:,.0f} - ${r_max:,.0f}"
        
        status_icon = "📍" if is_active else ""
        row_style = "background-color: rgba(0, 255, 163, 0.1);" if is_active else ""
        
        range_data.append({
            "Range Price": range_label,
            "Target BTC %": f"{r_target*100:.0f}%",
            "Status": status_icon
        })
        
        if is_active:
            target_alloc_now = r_target

    # Update Global State with new Target
    if state.get("target_allocation_btc") != target_alloc_now:
        state["target_allocation_btc"] = target_alloc_now
        save_state(state)
        st.rerun()

    st.dataframe(
        pd.DataFrame(range_data),
        hide_index=True,
        use_container_width=True,
        column_config={
            "Status": st.column_config.TextColumn(width="small")
        }
    )

    # RECOMENDAÇÃO (ACTION BOX)
    st.write("") # Spacer
    
    # Calculate Diff based on THE TABLE'S target (target_alloc_now), not the saved state (which might lag one rerun)
    req_btc_equity = total_portfolio_val * target_alloc_now
    diff_usd = req_btc_equity - total_btc_val
    diff_btc_qty = diff_usd / price if price else 0
    
    if abs(diff_usd) > 10: # $10 Threshold
        if diff_usd > 0:
            # COMPRA (BUY)
            box_color = "#FFF9C4" # Light Yellow
            border_color = "#FBC02D" # Gold
            text_color = "#F57F17"
            action_label = "COMPRA"
        else:
            # VENDA (SELL)
            box_color = "#E8F5E9" # Light Green
            border_color = "#43A047" # Green
            text_color = "#1B5E20"
            action_label = "VENDA"
            
        st.markdown(f"""
            <div style="
                border: 2px solid {border_color};
                background-color: {box_color};
                border-radius: 10px;
                padding: 15px;
                text-align: center;
                margin-top: 10px;
            ">
                <h2 style="color: {text_color}; margin: 0; font-weight: bold;">{action_label}</h2>
                <div style="font-size: 1.2rem; color: #333; margin-top: 5px;">
                    <b>${abs(diff_usd):,.0f}</b> <span style="font-size: 0.9rem; color: #555;">({abs(diff_btc_qty):.6f} BTC)</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="
                border: 2px solid #00C6FF;
                background-color: rgba(0, 198, 255, 0.1);
                border-radius: 10px;
                padding: 15px;
                text-align: center;
                margin-top: 10px;
            ">
                <h3 style="color: #00E5FF; margin: 0;">✅ BALANCEADO</h3>
            </div>
        """, unsafe_allow_html=True)

with col_right:
    # 4. CYCLE HISTORY
    st.subheader("📜 Cycle History")
    
    if state["deposits"]:
        # Reverse order for display
        history_df = pd.DataFrame(state["deposits"][::-1])
        st.dataframe(
            history_df,
            column_config={
                "cycle": "Ciclo",
                "type": "Status",
                "total_val": st.column_config.NumberColumn("Total", format="$%.2f"),
                "profit": st.column_config.NumberColumn("Lucro", format="$%.2f")
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("No cycles recorded.")
    
    # Undo Button
    if state["deposits"]:
        if st.button("↩️ Desfazer Último Ciclo"):
            removed = state["deposits"].pop()
            save_state(state)
            st.success(f"Ciclo {removed['cycle']} removido!")
            time.sleep(1)
            st.rerun()
        
    # Stats & Comparison
    st.markdown("### Performance Comparison")
    
    # Calculate HODL Strategy
    # Logic: Every 'DEPOSIT' is treated as an immediate BUY of BTC
    hold_btc_qty = 0.0
    total_invested_usd = 0.0
    
    for tx in state["deposits"]:
        if tx["type"] == "DEPOSIT":
             p = tx["price"] if tx["price"] > 0 else price
             amount = tx["usd_amount"]
             btc_bought = amount / p
             hold_btc_qty += btc_bought
             total_invested_usd += amount
             # Also add any direct BTC deposits if field exists (simple logic for now)
             if tx.get("btc_amount", 0) > 0 and tx["usd_amount"] == 0:
                 hold_btc_qty += tx["btc_amount"]
    
    hold_value = hold_btc_qty * price
    smart_value = total_portfolio_val
    
    pnl_hold = hold_value - total_invested_usd
    pnl_smart = smart_value - total_invested_usd
    
    k1, k2 = st.columns(2)
    k1.metric("Strategy (Smart)", f"${smart_value:,.2f}", delta=f"{pnl_smart:,.2f} PnL")
    k2.metric("Strategy (HODL)", f"${hold_value:,.2f}", delta=f"{pnl_hold:,.2f} PnL")

    # Telegram Automation
    from tools.send_alert import send_telegram_alert
    
    # Check for Alert Condition (Only if Action is Needed)
    # We use session state to track if we already sent an alert for this specific condition to avoid spam on refresh
    if "last_alert_msg" not in st.session_state:
        st.session_state["last_alert_msg"] = ""

    current_alert_msg = ""
    if abs(diff_usd) > 50: # Only alert on significant moves > $50
        action_type = "COMPRA" if diff_usd > 0 else "VENDA"
        current_alert_msg = f"🚨 *B.L.A.S.T. ALERT*\nPrice: ${price:,.0f}\nRange Target: {target_alloc_now*100:.0f}%\nAction: *{action_type}* ${abs(diff_usd):,.0f}"
    
    # Auto-Send if message changed (e.g. status flip)
    # Note: Streamlit re-runs on interaction, so this acts as a 'Check' on load.
    if current_alert_msg and current_alert_msg != st.session_state["last_alert_msg"]:
        if send_telegram_alert(current_alert_msg):
            st.toast("Telegram Notification Sent! 🚀")
            st.session_state["last_alert_msg"] = current_alert_msg
    elif not current_alert_msg:
        st.session_state["last_alert_msg"] = "" # Reset if balanced




    
    # Check Env Var

