# main.py

import time
from datetime import datetime
from phrase_library import PHRASES
from blog_scanner import fetch_blog_entries
from strike_engine import generate_strikes
from strike_queue import add_strike, get_confirmed_strikes
from odds_verification import verify_strikes_with_odds
from google_docs_writer import send_strike_to_doc
from multi_builder import detect_multi_opportunity
import requests
import json

# Constants
BLOG_FEED_URL = "https://feeds.bbci.co.uk/sport/football/rss.xml?edition=uk"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1367694718229811332/7_HAmXZYAkmfuWFrMQyvoBbcYX8GjhKeQofnwFcngXvtqKUFb14qhWtxjCOK42uiNpjw"
STRIKE_LOG_FILE = "strikes_log.json"

def post_to_discord(message):
    data = { "content": message }
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=data)
    except Exception as e:
        print("Discord post failed:", e)

def log_strike_json(strike):
    try:
        with open(STRIKE_LOG_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    strike["log_time"] = datetime.utcnow().isoformat() + "Z"
    data.append(strike)

    with open(STRIKE_LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def run_engine():
    print("Touarangi Engine – LIVE MODE")

    # 1. Fetch blog entries
    blog_entries = fetch_blog_entries(BLOG_FEED_URL)
    print(f"Scanned {len(blog_entries)} blog lines")

    # 2. Generate raw strikes
    raw_strikes = generate_strikes(blog_entries, PHRASES)

    # 3. Validate and confirm
    confirmed = []
    for strike in raw_strikes:
        verified = verify_strikes_with_odds(strike)
        if verified:
            add_strike(verified)
            send_strike_to_doc(verified)
            post_to_discord(
                f"**TOUARANGI STRIKE**\n"
                f"{verified['player']} – {verified['market']}\n"
                f"Odds: {verified['odds']} | Confidence: {verified['confidence']}%"
            )
            log_strike_json(verified)
            confirmed.append(verified)

    # 4. Check for live multi opportunities
    multi = detect_multi_opportunity(confirmed)
    if multi:
        send_strike_to_doc(multi)
        post_to_discord(
            f"**MULTI STRIKE**\n"
            f"{' + '.join(multi['legs'])}\n"
            f"Confidence: {multi['combined_confidence']}%"
        )
        log_strike_json(multi)

    print(f"[{datetime.utcnow().strftime('%H:%M:%S UTC')}] Cycle complete.\n")

if __name__ == "__main__":
    while True:
        run_engine()
        time.sleep(30)