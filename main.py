import time
from datetime import datetime
from phrase_library import PHRASES
from blog_scanner import fetch_blog_entries
from strike_engine import generate_strikes
from strike_queue import get_confirmed_strikes
from odds_verification import verify_strikes_with_odds
from google_docs_writer import send_strike_to_doc
from multi_builder import detect_multi_opportunity
import requests

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1367694718229811332/7_HAmXZYAkmfuWFrMQyvoBbcYX8GjhKeQofnwFcngXvtqKUFb14qhWtxjCOK42uiNpjw"
BLOG_FEED_URL = "https://feeds.bbci.co.uk/sport/football/rss.xml?edition=uk"

def post_to_discord(message):
    data = { "content": message }
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=data)
    except Exception as e:
        print("Discord post failed:", e)

def run_engine():
    print("Touarangi Engine (Live Blog Mode) running...")

    # Step 1: Fetch and scan blog
    blog_entries = fetch_blog_entries(BLOG_FEED_URL)
    print(f"Scanned {len(blog_entries)} blog lines")

    # Step 2: Run strike generation
    raw_strikes = generate_strikes(blog_entries, PHRASES)

    # Step 3: Validate and log strikes
    confirmed_strikes = []
    for strike in raw_strikes:
        verified = verify_strikes_with_odds(strike)
        if verified:
            confirmed_strikes.append(verified)
            send_strike_to_doc(verified)
            post_to_discord(
                f"**TOUARANGI STRIKE**\n"
                f"{verified.get('player', 'Unknown')} @ {verified.get('odds')}\n"
                f"Confidence: {verified.get('confidence')}%"
            )

    # Step 4: Check for live multi
    multi = detect_multi_opportunity(confirmed_strikes)
    if multi:
        send_strike_to_doc(multi)
        post_to_discord(
            f"**MULTI STRIKE**\n"
            f"Combined Confidence: {multi['combined_confidence']}%"
        )

    print(f"[{datetime.utcnow().strftime('%H:%M:%S')}] Cycle complete.\n")

if __name__ == "__main__":
    while True:
        run_engine()
        time.sleep(30)