import os
import requests
from dotenv import load_dotenv
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_test_message():
    if not TOKEN or not CHAT_ID:
        print("Error: Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID in .env")
        return

    clean_token = TOKEN.strip()
    url = f"https://api.telegram.org/bot{clean_token}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": "🚀 B.L.A.S.T. Protocol: Link Established. Telegram Connected."
    }
    
    print(f"Attempting to connect to Telegram API (SSL Verify=False)...")
    try:
        response = requests.post(url, json=payload, timeout=10, verify=False)
        if response.status_code == 200:
             print("Success! Message sent to Telegram.")
             print(response.json())
        else:
            print(f"Failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error executing request: {e}")

if __name__ == "__main__":
    send_test_message()
