
import os
import requests
from flask import Flask
from datetime import datetime, timedelta

app = Flask(__name__)

# Load secret environment variables
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

def get_recent_telegram_links():
    """Fetches recent messages from the Telegram channel to check for duplicates."""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?limit=20"
        response = requests.get(url).json()
        
        posted_links = []
        if response.get("ok"):
            for result in response.get("result", []):
                message = result.get("channel_post", {}).get("text", "")
                for word in message.split():
                    if word.startswith("http"):
                        posted_links.append(word)
        return posted_links
    except Exception:
        return []

@app.route('/')
@app.route('/trigger')
def trigger_bot():
    # 1. Look back 120 minutes to beat the API cache delay
    time_threshold = datetime.utcnow() - timedelta(minutes=1440)


    # 2. Fetch tech news 
    url = f"https://newsapi.org/v2/top-headlines?category=technology&language=en&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()
    articles = response.get("articles", [])

    # 3. Filter for articles in the time window
    fresh_articles = []
    for art in articles:
        pub_time_str = art.get("publishedAt")
        if pub_time_str:
            clean_time_str = pub_time_str.replace("Z", "")
            pub_time = datetime.fromisoformat(clean_time_str)
            
            if pub_time > time_threshold:
                fresh_articles.append(art)

    if not fresh_articles:
        return "No new articles found in the last 2 hours.", 200

    # 4. Fetch already posted links from Telegram to avoid duplicates
    already_posted = get_recent_telegram_links()

    # 5. Build the news report list with strictly UNIQUE articles
    report = "Latest Fresh Tech News:\n"
    count = 1
    new_stories_added = False
    
    for art in fresh_articles:
        title = art.get("title")
        link = art.get("url")
        
        if title and link:
            if link in already_posted:
                continue
                
            report += f"\n{count}. {title}\nLink: {link}\n"
            count += 1
            new_stories_added = True
            
        if count > 5:
            break

    if not new_stories_added:
        return "All articles in the window were already posted.", 200

    # 6. Send to Telegram
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": report,
        "disable_web_page_preview": False
    }
    
    requests.post(telegram_url, json=payload)
    return "Bot executed successfully with fresh, non-duplicate news!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
