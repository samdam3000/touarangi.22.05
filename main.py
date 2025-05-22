import json
import requests
from datetime import datetime

from phrase_library import PHRASES
from blog_scanner import fetch_blog_entries
from strike_engine import generate_strikes
from strike_queue import add_strike, get_confirmed_strikes
from odds_verification import verify_strikes_with_odds
from multi_builder import detect_multi_opportunity
from logger import log_info, log_strike_summary

# --- LIVE FEED SETUP ---
BLOG_FEED_URL = "https://feeds.bbci.co.uk/sport/football/rss.xml?edition=uk"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1367694718229811332/7_HAmXZYAkmfuWFrMQyvoBbcYX8GjhKeQofnwFcngXvtqKUFb14qhWtxjCOK42uiNpjw"
STRIKE_LOG_FILE = "strikes_log.json"

last_multi_fired = None  # cooldown tracker

print(">>> TOUARANGI STARTED at", datetime.utcnow().isoformat())

def post_to_discord(message):
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
        if response.status_code != 204:
            print("[DISCORD ERROR]", response.status_code, response.text)
    except Exception as e:
        print("[DISCORD EXCEPTION]", e)

    print(f"[STRIKE ALERT] {message}")

def log_strike_json(strike):
    try:
        with open(STRIKE_LOG_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    strike["log_time"] = datetime.utcnow().isoformat() + "Z"
    data.append(strike)

    with open(STRIKE_LOG_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)

def run_engine():
    global last_multi_fired

    print(">>> Engine running:", datetime.utcnow().isoformat())
    blog_entries = fetch_blog_entries(BLOG_FEED_URL)
    print(f">>> Blog entries found: {len(blog_entries)}")

    raw_strikes = generate_strikes(blog_entries, PHRASES)
    print(f">>> Raw strikes generated: {len(raw_strikes)}")

    confirmed = []

    for strike in raw_strikes:
        verified = verify_strikes_with_odds(strike)
        if not verified:
            continue

        add_strike(verified)
        post_to_discord(
            f"**TOUARANGI STRIKE**\n"
            f"{verified['player']} - {verified['market']}\n"
            f"Odds: {verified['odds']} | Confidence: {verified['confidence']}%"
        )
        log_strike_json(verified)
        log_strike_summary(verified)
        confirmed.append(verified)

    print(f">>> Confirmed strikes sent: {len(confirmed)}")

    multi = detect_multi_opportunity(get_confirmed_strikes())
    if multi:
        now = datetime.utcnow()
        if not last_multi_fired or (now - last_multi_fired).seconds > 180:
            post_to_discord(
                f"**MULTI STRIKE**\n"
                f"{' + '.join(multi['legs'])}\n"
                f"Combined Confidence: {multi['combined_confidence']}%"
            )
            log_strike_json(multi)
            log_strike_summary(multi)
            last_multi_fired = now

    print(">>> Engine finished.\n")

# RUN once
try:
    run_engine()
except Exception as e:
    print("[FATAL ERROR]", e)