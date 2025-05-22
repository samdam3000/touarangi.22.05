import time
import json
import requests
from datetime import datetime

from phrase_library import PHRASES
from blog_scanner import fetch_blog_entries
from strike_engine import generate_strikes
from strike_queue import add_strike, get_confirmed_strikes
from odds_verification import verify_strikes_with_odds  # Connected to real scraper
from multi_builder import detect_multi_opportunity
from logger import log_info, log_strike_summary
from google_docs_writer import send_strike_to_doc

# --- LIVE FEED SETUP ---
BLOG_FEED_URL = "https://feeds.bbci.co.uk/sport/football/rss.xml?edition=uk"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1367694718229811332/7_HAmXZYAkmfuWFrMQyvoBbcYX8GjhKeQofnwFcngXvtqKUFb14qhWtxjCOK42uiNpjw"
STRIKE_LOG_FILE = "strikes_log.json"

print(">>> TOUARANGI STARTED at", datetime.utcnow().isoformat())

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
