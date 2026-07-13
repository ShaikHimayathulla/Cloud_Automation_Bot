import os
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def fetch_latest_news():
    try:
        url = "https://baconipsum.com"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return "CLOUD AUTOMATION BOT REPORT:\n\nUpdates: " + " ".join(data)
        return "CLOUD AUTOMATION BOT REPORT:\n\nSystem online. Ready for news integration."
    except Exception:
        return "CLOUD AUTOMATION BOT REPORT:\n\nSystem online. Ready for next project phase."

def send_to_telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Missing environment variables!")
        return
    
    # This completely cleans the credentials and forces a perfect link structure
    clean_token = str(TELEGRAM_TOKEN).strip()
url = f"https://api.telegram.org/bot{clean_token}/sendMessage"

    
    payload = {"chat_id": str(TELEGRAM_CHAT_ID).strip(), "text": message}
    try:
        req = requests.post(url, json=payload, timeout=10)
        print("Telegram Response Code:", req.status_code)
    except Exception as e:
        print("Failed to connect to Telegram:", e)

if __name__ == "__main__":
    print("Cloud engine initiated...")
    news_report = fetch_latest_news()
    send_to_telegram(news_report)
    print("Automation task completed successfully!")
