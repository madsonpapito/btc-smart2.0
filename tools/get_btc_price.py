import requests
import sys

def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        price = data['bitcoin']['usd']
        return price
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

if __name__ == "__main__":
    price = get_btc_price()
    if price:
        print(f"BTC Price: ${price}")
    else:
        sys.exit(1)
