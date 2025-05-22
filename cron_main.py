import time
import json
import requests
from datetime import datetime

# Replace these with your real modules if needed
from phrase_library import PHRASES
from blog_scanner import fetch_blog_entries
from strike_engine import generate_strikes
from strike_queue import add_strike, get_confirmed_strikes
from odds_verification import verify_strikes_with_odds
from multi_builder import detect_multi_opportunity
from logger import log_info, log_strike_summary
from google_docs_writer import send_strike_to_doc

BLOG_FEED_URL = "https://feeds.bbci.co.uk/sport/football/rss.xml?edition=uk"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1367694718229811332/7_HAmXZYAkmfuWFrMQyvoBbcYX8GjhKeQofnwFcngXvtqKUFb14qhWtxjCOK42uiNpjw"
STRIKE_LOG_FILE = "strikes_log.json"

print(">>> TOUARANGI CRON STARTED at", datetime.utcnow().isoformat())

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

        add_strike(verified)
        post_to_discord(
            f"**TOUARANGI STRIKE**\\n"
            f"{verified['player']} – {verified['market']}\\n"
            f"Odds: {verified['odds']} | Confidence: {verified['confidence']}%"
        )
        send_strike_to_doc(verified)
        log_strike_json(verified)
        log_strike_summary(verified)
        confirmed.append(verified)

    multi = detect_multi_opportunity(get_confirmed_strikes())
    if multi:
        post_to_discord(
            f"**MULTI STRIKE**\\n"
            f"{' + '.join(multi['legs'])}\\n"
            f"Combined Confidence: {multi['combined_confidence']}%"
        )
        log_strike_json(multi)
        log_strike_summary(multi)

    log_info(">>> Cycle complete.\\n")

def cron_loop():
    while True:
        try:
            run_engine()
        except Exception as e:
            print("[CRON ERROR]", e)
        time.sleep(30)

if __name__ == "__main__":
    cron_loop()