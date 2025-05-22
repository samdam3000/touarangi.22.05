# strike_engine.py

from correct_score import evaluate_correct_score_tennis
from set_winner import evaluate_set_winner_from_blog
from over_under import evaluate_over_under_from_blog
from timing import get_utc_time

def generate_strikes(blog_lines, phrase_list):
    """
    Master strike builder: processes blog lines and outputs fire-ready strike objects.
    """
    strikes = []

    for line in blog_lines:
        text = line.lower()

        # --- Phrase Trigger (General Momentum) ---
        matched_phrases = [p for p in phrase_list if p in text]
        if matched_phrases:
            strike = {
                "market": "Momentum Trigger",
                "player": detect_player_name(text),
                "confidence": base_confidence(matched_phrases),
                "reason": f"Matched phrases: {', '.join(matched_phrases)}",
                "confirmed_time": get_utc_time(),
                "strike_type": "LOCK"
            }
            strikes.append(strike)

        # --- Set Winner (Tennis) ---
        set_result = evaluate_set_winner_from_blog(text)
        if set_result:
            set_result.update({
                "player": detect_player_name(text),
                "confirmed_time": get_utc_time(),
                "strike_type": "LOCK"
            })
            strikes.append(set_result)

        # --- Correct Score (Tennis) ---
        score_result = evaluate_correct_score_tennis(text)
        if score_result:
            score_result.update({
                "player": detect_player_name(text),
                "confirmed_time": get_utc_time(),
                "strike_type": "LOCK"
            })
            strikes.append(score_result)

        # --- Over/Under (All Sports) ---
        ou_result = evaluate_over_under_from_blog(text)
        if ou_result:
            ou_result.update({
                "player": "Global Total",  # not player-specific
                "confirmed_time": get_utc_time(),
                "strike_type": "LOCK"
            })
            strikes.append(ou_result)

    return strikes

def base_confidence(phrases):
    """
    Phrase-based confidence weighting.
    """
    high_weight = {"dominant", "collapse", "storming", "rattled", "folding", "relentless"}
    count = len(phrases)
    boost = sum(1 for p in phrases if any(h in p for h in high_weight))
    return min(90, 70 + (count * 2) + (boost * 3))

def detect_player_name(text):
    """
    Basic name recognition — expand with team sheets or live player references.
    """
    if "swiatek" in text:
        return "Iga Swiatek"
    if "alcaraz" in text:
        return "Carlos Alcaraz"
    if "arsenal" in text:
        return "Arsenal"
    if "man united" in text:
        return "Man United"
    if "storm" in text:
        return "Melbourne Storm"
    if "roosters" in text:
        return "Sydney Roosters"
    return "Unknown"