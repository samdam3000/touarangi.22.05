# odds_verification.py

from bet365_scraper import fetch_live_odds
import json
from datetime import datetime

DEBUG_LOG = "debug_odds.json"

def verify_strikes_with_odds(strike, min_confidence=65, max_odds=2.80):
    """
    Checks if a strike is valid based on live odds and confidence.
    Adds odds to the strike and logs it if confirmed.
    """
    player = strike.get("player", "Unknown")
    confidence = strike.get("confidence", 0)

    # Skip if below minimum confidence
    if confidence < min_confidence:
        return None

    # Fetch odds
    odds = fetch_live_odds(player)
    if odds is None or odds > max_odds:
        return None

    # Attach odds
    strike["odds"] = odds

    # Log to debug file
    log_odds_debug(player, odds, source="live")

    return strike


def log_odds_debug(player, odds, source="live"):
    """
    Writes player odds to debug_odds.json with timestamp.
    """
    try:
        with open(DEBUG_LOG, "r") as f:
            data = json.load(f)
    except:
        data = {}

    data[player] = {
        "source": source,
        "last_odds": odds,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    with open(DEBUG_LOG, "w") as f:
        json.dump(data, f, indent=2)