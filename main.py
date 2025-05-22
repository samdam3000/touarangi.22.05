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

print(">>> TOUARANGI STARTED at", datetime.utcnow().isoformat())

def post_to_discord(message):
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
        if response.status_code != 204:
            print("[DISCORD ERROR] Status:", response.status_code, "| Message:", response.text)
    except Exception as e:
        print("[DISCORD EXCEPTION]", e)

# Test webhook connectivity
post_to_discord(">>> TESTING DISCORD WEBHOOK â€” Touarangi is alive.")

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
    log_info(">>> run_engine() triggered at " + datetime.utcnow().isoformat())

    blog_entries = fetch_blog_entries(BLOG_FEED_URL)
    if not blog_entries:
        log_info(">>> No blog entries retrieved.")
        return

    raw_strikes = generate_strikes(blog_entries, PHRASES)
    confirmed = []

    for strike in raw_strikes:
        verified = verify_strikes_with_odds(strike)
        if not verified:
            continue

        print(">>> STRIKE VERIFIED:", verified)

        add_strike(verified)
        post_to_discord(
            f"**TOUARANGI STRIKE**\n"
            f"{verified['player']} â€“ {verified['market']}\n"
            f"Odds: {verified['odds']} | Confidence: {verified['confidence']}%"
        )
        log_strike_json(verified)
        log_strike_summary(verified)
        confirmed.append(verified)

    multi = detect_multi_opportunity(get_confirmed_strikes())
    if multi:
        post_to_discord(
            f"**MULTI STRIKE**\n"
            f"{' + '.join(multi['legs'])}\n"
            f"Combined Confidence: {multi['combined_confidence']}%"
        )
        log_strike_json(multi)
        log_strike_summary(multi)

    log_info(">>> Cycle complete.\n")

# Optional: Force a fake test strike to validate Discord + logger
def inject_fake_strike():
    fake = {
        "player": "Test Player",
        "market": "Anytime Goalscorer",
        "odds": 3.20,
        "confidence": 88
    }
    add_strike(fake)
    post_to_discord(
        f"**TOUARANGI STRIKE**\n"
        f"{fake['player']} â€“ {fake['market']}\n"
        f"Odds: {fake['odds']} | Confidence: {fake['confidence']}%"
    )
    log_strike_json(fake)
    log_strike_summary(fake)
    log_info(">>> FAKE STRIKE INJECTED")

# RUN
try:
    run_engine()
    inject_fake_strike()  # remove this after confirming it works
except Exception as e:
    print("[FATAL ERROR]", e)