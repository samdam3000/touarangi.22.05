# main.py

import time
import json
import requests
from datetime import datetime

from phrase_library import PHRASES
from strike_engine import generate_strikes
from strike_queue import add_strike, get_confirmed_strikes
from odds_verification import verify_strikes_with_odds
from multi_builder import detect_multi_opportunity
from logger import log_info, log_strike_summary

# Use test lines instead of feed
blog_entries = [
    "Swiatek storming through the set, no resistance left",
    "Alcaraz relentless with dominant first serve",
    "This has become a goal fest — wide open at both ends",
    "Tight battle, holding serve easily but no real chances",
]

# Your webhook
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
    log_info("TOUARANGI TEST CYCLE")

    raw_strikes = generate_strikes(blog_entries, PHRASES)
    confirmed = []

    for strike in raw_strikes:
        verified = verify_strikes_with_odds(strike)
        if verified:
            add_strike(verified)
            post_to_discord(
                f"**TOUARANGI STRIKE**\n"
                f"{verified['player']} – {verified['market']}\n"
                f"Odds: {verified.get('odds', '?')} | Confidence: {verified['confidence']}%"
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

    log_info("Cycle complete.\n")

if __name__ == "__main__":
    run_engine()