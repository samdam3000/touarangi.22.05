# bet365_scraper.py

import requests

API_KEY = "6703de1c9e2bee97a99fb43948930ab2"
SPORT = "soccer_epl"  # can also use "tennis"
REGION = "uk"
MARKET = "h2h"

def fetch_live_odds(player_name=None):
    url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds"
    params = {
        "apiKey": API_KEY,
        "regions": REGION,
        "markets": MARKET,
        "oddsFormat": "decimal"
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            for game in data:
                for bookmaker in game.get("bookmakers", []):
                    if bookmaker["title"].lower() == "bet365":
                        for market in bookmaker.get("markets", []):
                            for outcome in market.get("outcomes", []):
                                if player_name and player_name.lower() in outcome["name"].lower():
                                    return outcome["price"]
            return None
        else:
            print("API error:", response.status_code, response.text)
            return None
    except Exception as e:
        print("Odds fetch failed:", e)
        return None