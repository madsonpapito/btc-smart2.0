import os
import requests
import urllib3
from dotenv import load_dotenv

# Suppress InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Suppress InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def send_telegram_alert(message):
    # Load env vars safely here
    load_dotenv(override=True)
    
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    if not TOKEN or not CHAT_ID:
        print("Telegram credentials missing.")
        return False
        
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload, verify=False, timeout=5)
        return response.ok
    except Exception as e:
        print(f"Telegram Error: {e}")
        return False

if __name__ == "__main__":
    send_telegram_alert("⚠️ *TEST MESSAGE* from Dashboard Logic")
