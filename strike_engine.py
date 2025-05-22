# strike_engine.py

from correct_score import evaluate_correct_score_tennis

def generate_strikes(blog_lines, phrase_list):
    """
    Scans blog lines for key phrases and overlays, then outputs structured strike objects.
    """
    strikes = []

    for line in blog_lines:
        text = line.lower()

        # --- Phrase Match Core ---
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

        # --- Correct Score Analysis (Tennis Only) ---
        score_result = evaluate_correct_score_tennis(text)
        if score_result:
            score_result.update({
                "market": "Correct Score",
                "player": detect_player_name(text),
                "confirmed_time": get_utc_time(),
                "strike_type": "LOCK"
            })
            strikes.append(score_result)

    return strikes

def base_confidence(phrases):
    """
    Returns a baseline confidence score depending on phrase strength and quantity.
    """
    high_weight = {"dominant", "collapse", "no resistance", "storming"}
    count = len(phrases)
    boost = sum(1 for p in phrases if any(h in p for h in high_weight))
    return min(90, 70 + (count * 2) + (boost * 3))

def detect_player_name(text):
    """
    Very basic placeholder. Replace with proper NLP parsing or blog context.
    """
    if "swiatek" in text:
        return "Iga Swiatek"
    if "alcaraz" in text:
        return "Carlos Alcaraz"
    if "arsenal" in text:
        return "Arsenal"
    if "man united" in text:
        return "Man United"
    return "Unknown"

def get_utc_time():
    from datetime import datetime
    return datetime.utcnow()