import requests
import sys

def get_btc_price():
    # Attempt 1: Coinbase (Very Reliable)
    try:
        url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
        response = requests.get(url, timeout=5)
        data = response.json()
        return float(data['data']['amount'])
    except Exception:
        pass

    # Attempt 2: Binance (High Volume)
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        response = requests.get(url, timeout=5)
        data = response.json()
        return float(data['price'])
    except Exception:
        pass

    # Attempt 3: CoinGecko (Fallback)
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url, timeout=5)
        data = response.json()
        return float(data['bitcoin']['usd'])
    except Exception:
        pass

    return None

if __name__ == "__main__":
    price = get_btc_price()
    if price:
        print(f"BTC Price: ${price}")
    else:
        sys.exit(1)
