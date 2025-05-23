# main.py

from blog_scanner import scan_blogs
from phrase_library import load_vocabulary
from strike_engine import evaluate_strikes
from odds_verification import attach_odds_and_tier
from logger import log_strike_to_discord, log_summary
from strike_queue import is_duplicate_strike, store_strike
import time

REFRESH_INTERVAL = 60  # Seconds between scans

def main():
    print("TOUARANGI SYSTEM STARTED")
    vocabulary = load_vocabulary()

    while True:
        print("Scanning blogs...")
        blog_data = scan_blogs()

        print("Evaluating strike candidates...")
        strike_candidates = evaluate_strikes(blog_data, vocabulary)

        for strike in strike_candidates:
            if not is_duplicate_strike(strike):
                strike = attach_odds_and_tier(strike)
                store_strike(strike)
                log_strike_to_discord(strike)
                log_summary(strike)

        print("Sleeping before next scan...")
        time.sleep(REFRESH_INTERVAL)

if __name__ == "__main__":
    main()