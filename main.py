# main.py

import time
import json
import requests
from datetime import datetime

from phrase_library import PHRASES
from blog_scanner import fetch_blog_entries
from strike_engine import generate_strikes
from strike_queue import add_strike, get_confirmed_strikes
from odds_verification import verify_strikes_with_odds
from google_docs_writer import send_strike_to_doc
from multi_builder import detect_multi_opportunity
from logger import log_info, log_strike_summary

# Settings
BLOG_FEED_URL = "https://feeds.bbci.co.uk/sport/football/rss.xml?edition=uk"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1367694718229811332/7_HAmXZYAkmfuWFrMQyvoBbcYX8GjhKeQofnwFcngXvtqKUFb14qhWtxjCOK42uiNpjw"
STRIKE_LOG_FILE = "strikes_log.json"

def post_to_discord(message):
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print("[DISCORD ERROR]", e)

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
    log_info("Starting Touarangi scan...")

    # 1. Pull blog lines
    blog_entries = fetch_blog_entries(BLOG_FEED_URL)
    log_info(f"Fetched {len(blog_entries)} blog lines")

    # 2. Generate potential strikes
    raw_strikes = generate_strikes(blog_entries, PHRASES)

    # 3. Confirm strikes with odds validation
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
            log_strike_summary(verified)
            confirmed.append(verified)

    # 4. Check for multi-strike combos
    multi = detect_multi_opportunity(get_confirmed_strikes())
    if multi:
        send_strike_to_doc(multi)
        post_to_discord(
            f"**MULTI STRIKE**\n"
            f"{' + '.join(multi['legs'])}\n"
            f"Combined Confidence: {multi['combined_confidence']}%"
        )
        log_strike_json(multi)
        log_strike_summary(multi)

    log_info("Touarangi cycle complete.\n")

if __name__ == "__main__":
    while True:
        run_engine()
        time.sleep(30)