import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
# Basescan Native Endpoint
BASESCAN_API_URL = "https://api.basescan.org/api"

# Token Contract Addresses (Lower case for comparison)
TOKENS = {
    "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913": "USDC",
    "0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf": "cbBTC",
    "0x4200000000000000000000000000000000000006": "WETH"
}

def fetch_history():
    if not WALLET_ADDRESS:
        print("Error: WALLET_ADDRESS not found in .env")
        return []

    print(f"Fetching history for {WALLET_ADDRESS}...")
    
    # Fetch Token Transfers via Basescan Native
    apikey = os.getenv("BASESCAN_API_KEY")
    params = {
        "module": "account",
        "action": "tokentx",
        "address": WALLET_ADDRESS,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": apikey
    }
    
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(BASESCAN_API_URL, params=params, headers=headers, timeout=10)
        data = response.json()
        
        if data["status"] != "1":
            print(f"Basescan Error or No Data: {data.get('message')}")
            return []
            
        raw_txs = data["result"]
        cycles = []
        
        # Process Transactions into "Cycles"
        # Logic: If receiving USDC -> DEPOSIT? If sending USDC -> BUY? 
        # This is complex because Swaps look like Output USDC + Input BTC in same block.
        # Capability limitation: We see transfers. We'll group by transactionHash.
        
        tx_grouped = {}
        for tx in raw_txs:
            h = tx["hash"]
            if h not in tx_grouped:
                tx_grouped[h] = []
            tx_grouped[h].append(tx)
            
        cycle_count = 1
        
        for tx_hash, transfers in tx_grouped.items():
            # Analyze the bundle of transfers in this hash
            # Heuristics:
            # 1. In: USDC, Out: None -> Deposit
            # 2. Out: USDC, In: BTC -> BUY
            # 3. Out: BTC, In: USDC -> SELL
            
            summary = {"in": {}, "out": {}}
            ts = int(transfers[0]["timeStamp"])
            date_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
            
            for t in transfers:
                token = TOKENS.get(t["contractAddress"].lower())
                if not token: continue # Skip irrelevant tokens
                
                val = float(t["value"]) / (10 ** int(t["tokenDecimal"]))
                
                if t["to"].lower() == WALLET_ADDRESS.lower():
                    summary["in"][token] = summary["in"].get(token, 0) + val
                elif t["from"].lower() == WALLET_ADDRESS.lower():
                    summary["out"][token] = summary["out"].get(token, 0) + val
            
            # Decide Type
            type_str = "UNKNOWN"
            btc_amt = 0
            usd_amt = 0
            
            # Case: Deposit USDC
            if "USDC" in summary["in"] and not summary["out"]:
                type_str = "DEPOSIT"
                usd_amt = summary["in"]["USDC"]
                
            # Case: BUY (Out USDC, In BTC)
            elif "USDC" in summary["out"] and ("cbBTC" in summary["in"] or "WBTC" in summary["in"]):
                type_str = "BUY"
                usd_amt = summary["out"]["USDC"]
                btc_amt = summary["in"].get("cbBTC", 0) + summary["in"].get("WBTC", 0)
                
            # Case: SELL (Out BTC, In USDC)
            elif ("cbBTC" in summary["out"] or "WBTC" in summary["out"]) and "USDC" in summary["in"]:
                type_str = "SELL"
                usd_amt = summary["in"]["USDC"]
                btc_amt = summary["out"].get("cbBTC", 0) + summary["out"].get("WBTC", 0)
                
            if type_str != "UNKNOWN":
                cycles.append({
                    "cycle": cycle_count,
                    "type": type_str,
                    "date": date_str,
                    "btc_amount": btc_amt,
                    "usd_amount": usd_amt,
                    "price": (usd_amt / btc_amt) if btc_amt > 0 else 0, # Implied Price
                    "total_val": usd_amt if type_str == "DEPOSIT" else 0, # Placeholder
                    "profit": 0,
                    "tx_hash": tx_hash
                })
                cycle_count += 1
                
        return cycles

    except Exception as e:
        print(f"Error fetching history: {e}")
        return []

if __name__ == "__main__":
    c = fetch_history()
    print(json.dumps(c, indent=2))
