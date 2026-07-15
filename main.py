import os
import requests
from flask import Flask

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

@app.route('/')
@app.route('/trigger')
def trigger_bot():
    # Fetch news from TechCrunch's official free RSS-to-JSON API (No API key needed, never blocks Render!)
    url = "https://api.rss2json.com/v1/api.json?rss_url=https://techcrunch.com/feed/"
    
    try:
        response = requests.get(url).json()
        articles = response.get("items", [])
    except Exception as e:
        return f"Failed to fetch RSS news feed: {str(e)}", 500

    if not articles:
        return "No tech news found in the RSS feed right now.", 200

    # Build report (grabs the top 5 stories)
    report = "Latest Breaking Tech News:\n"
    count = 1
    
    for art in articles:
        title = art.get("title")
        link = art.get("link")
        
        if title and link:
            report += f"\n{count}. {title}\nLink: {link}\n"
            count += 1
            
        if count > 5:
            break

    # Send directly to Telegram
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


