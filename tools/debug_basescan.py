import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
BASESCAN_API_KEY = os.getenv("BASESCAN_API_KEY")
BASESCAN_API_URL = "https://api.etherscan.io/v2/api"

def debug_basescan():
    print(f"Key: {BASESCAN_API_KEY}")
    params = {
        "chainid": 8453,
        "module": "account",
        "action": "tokentx",
        "address": WALLET_ADDRESS,
        "apikey": BASESCAN_API_KEY
    }
    
    try:
        response = requests.get(BASESCAN_API_URL, params=params)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_basescan()
