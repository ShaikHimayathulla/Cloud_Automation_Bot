import os
import requests
from flask import Flask
from datetime import datetime, timedelta

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

@app.route('/')
@app.route('/trigger')
def trigger_bot():
    # 1. Look back 24 hours to ensure we ALWAYS find news
    time_threshold = datetime.utcnow() - timedelta(minutes=1440)

    # 2. Fetch tech news
    url = f"https://newsapi.org/v2/top-headlines?category=technology&language=en&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()
    articles = response.get("articles", [])

    # 3. Filter for fresh articles
    fresh_articles = []
    for art in articles:
        pub_time_str = art.get("publishedAt")
        if pub_time_str:
            clean_time_str = pub_time_str.replace("Z", "")
            pub_time = datetime.fromisoformat(clean_time_str)
            if pub_time > time_threshold:
                fresh_articles.append(art)

    if not fresh_articles:
        return "No tech news found in the global feed for the last 24 hours.", 200

    # 4. Build report (grabs the top 5 stories)
    report = "Latest Breaking Tech News:\n"
    count = 1
    
    for art in fresh_articles:
        title = art.get("title")
        link = art.get("url")
        
        if title and link:
            report += f"\n{count}. {title}\nLink: {link}\n"
            count += 1
            
        if count > 5:
            break

    # 5. Send directly to Telegram
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": report,
        "disable_web_page_preview": False
    }
    
    requests.post(telegram_url, json=payload)
    return "Bot successfully pushed top global news to Telegram!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

