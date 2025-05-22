# over_under.py

def evaluate_over_under_from_blog(blog_text):
    """
    Predicts over/under trigger from blog line language.
    Returns a strike dict with market, confidence, and reason.
    """

    text = blog_text.lower()

    # --- Strong OVER indicators ---
    if any(kw in text for kw in [
        "frenetic pace", "wide open game", "all out attack", "trading blows",
        "fireworks", "end to end", "goal fest", "high tempo", "fast rallies",
        "explosive start", "racing through sets", "big hitting"
    ]):
        return {
            "market": "Total Points/Goals – OVER",
            "confidence": 80,
            "reason": "High-pace and offensive tone"
        }

    # --- Mild OVER (pending conversion) ---
    if any(kw in text for kw in [
        "lots of chances", "wave after wave", "tight defense broken",
        "rally after rally", "piling pressure", "testing the keeper"
    ]):
        return {
            "market": "Total Points/Goals – OVER",
            "confidence": 72,
            "reason": "Persistent attacking tone"
        }

    # --- Strong UNDER indicators ---
    if any(kw in text for kw in [
        "no real chances", "locked up", "cagey", "tight opening",
        "scrappy game", "slow start", "both sides cautious", "defensive slugfest",
        "can't hit through", "holding serve comfortably", "flat rhythm"
    ]):
        return {
            "market": "Total Points/Goals – UNDER",
            "confidence": 78,
            "reason": "Low-tempo or suppression tone"
        }

    # --- Mild UNDER signals ---
    if any(kw in text for kw in [
        "early nerves", "midfield battle", "lots of errors", "sloppy finish",
        "neither side settled", "deadlock"
    ]):
        return {
            "market": "Total Points/Goals – UNDER",
            "confidence": 70,
            "reason": "Early low-threat dynamics"
        }

    return None