import os
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def fetch_latest_news():
    url = "https://spaceflightnewsapi.net"
    response = requests.get(url).json()
    
    formatted_text = "CLOUD AUTOMATION BOT REPORT:\n\n"
    for article in response['results']:
        formatted_text += "Title: " + str(article['title']) + "\nLink: " + str(article['url']) + "\n\n"
    return formatted_text

def send_to_telegram(message):
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, json=payload)

if __name__ == "__main__":
    print("Cloud engine initiated...")
    news_report = fetch_latest_news()
    send_to_telegram(news_report)
    print("Automation task completed and sent to mobile successfully!")
