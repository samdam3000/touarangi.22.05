logger.py

import logging import requests

Discord webhook

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK"

Known sport-specific markets

VALID_MARKETS = { 'football': ['Anytime Goalscorer', 'First Goalscorer', '2+ Goals', 'Next Goal', 'Team to Score'], 'tennis': ['Set Winner', 'Next Game Winner', 'Over/Under Games'], 'cricket': ['Top Runscorer', 'Next Wicket', 'Over Total Runs'], }

Map entity keywords to sport

SPORT_CONTEXT = { 'rashford': 'football', 'denmark': 'football', 'djokovic': 'tennis', 'walsh': 'football', 'crawley': 'football', 'geneva': 'tennis', 'kohli': 'cricket', 'england': 'cricket', 'warner': 'cricket', }

Suggested default markets by sport

DEFAULT_MARKET = { 'football': 'Anytime Goalscorer', 'tennis': 'Set Winner', 'cricket': 'Top Runscorer', }

def determine_sport(entity: str) -> str: entity_key = entity.lower().split()[0] return SPORT_CONTEXT.get(entity_key, 'unknown')

def validate_strike(entity: str, market: str) -> bool: sport = determine_sport(entity) if sport == 'unknown': return False return market in VALID_MARKETS.get(sport, [])

def autocorrect_market(entity: str) -> str: sport = determine_sport(entity) return DEFAULT_MARKET.get(sport, 'Unknown Market')

def format_strike_output(entity: str, market: str, odds: float, confidence: float) -> str: if not validate_strike(entity, market): corrected_market = autocorrect_market(entity) if corrected_market == 'Unknown Market': return f"INVALID STRIKE FILTERED: {entity} - {market} ({odds}, {confidence}%)" market = corrected_market  # replace with default valid market

return (
    f"**TOUARANGI STRIKE**\n"
    f"{entity} – {market}\n"
    f"Odds: {odds} | Confidence: {confidence}%"
)

def send_to_discord(message: str): payload = {"content": message} try: response = requests.post(DISCORD_WEBHOOK_URL, json=payload) response.raise_for_status() except requests.exceptions.RequestException as e: logging.error(f"Failed to send message to Discord: {e}")

def log_strike(entity: str, market: str, odds: float, confidence: float): message = format_strike_output(entity, market, odds, confidence) if not message.startswith("INVALID"): send_to_discord(message) else: logging.info(message)

