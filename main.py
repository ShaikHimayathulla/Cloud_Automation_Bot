
import os
import requests
from flask import Flask

app = Flask(__name__)

def fetch_latest_news():
    try:
        api_key = os.getenv("NEWS_API_KEY")
        if not api_key:
            return "CLOUD AUTOMATION BOT REPORT:\n\nError: Missing NEWS_API_KEY in environment variables."

        url = f"https://newsapi.org/v2/top-headlines?category=technology&language=en&apiKey={api_key}"
        headers = {"User-Agent": "CloudAutomationBot/1.0"}
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            
            if not articles:
                return "CLOUD AUTOMATION BOT REPORT:\n\nNo new articles found right now."
                
            report = "CLOUD AUTOMATION BOT REPORT:\n\nLatest Tech News:\n"
            for i, article in enumerate(articles[:3], 1):
                title = article.get("title")
                link = article.get("url")
                report += f"\n{i}. {title}\nLink: {link}\n"
                
            return report
        else:
            return f"CLOUD AUTOMATION BOT REPORT:\n\nFailed to fetch news. Status code: {response.status_code}"
            
    except Exception as e:
        return f"CLOUD AUTOMATION BOT REPORT:\n\nError fetching news: {str(e)}"

def send_to_telegram(message):
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Missing variables!")
        return

    url = f"https://api.telegram.org/bot{str(TELEGRAM_TOKEN).strip()}/sendMessage"
    payload = {"chat_id": str(TELEGRAM_CHAT_ID).strip(), "text": message}
    requests.post(url, json=payload, timeout=10)

@app.route('/')
@app.route('/trigger')
def trigger_bot():
    news_report = fetch_latest_news()
    send_to_telegram(news_report)
    return "Bot executed successfully!", 200

if __name__ == "__main__":
    # Notice the 4 spaces of indentation below!
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
