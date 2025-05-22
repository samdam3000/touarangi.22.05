# set_winner.py

def evaluate_set_winner_from_blog(blog_text):
    """
    Predicts the likely winner of the current set based on blog language.
    Returns a prediction dict with player, market, confidence, and reason.
    """

    text = blog_text.lower()

    if any(kw in text for kw in ["has broken", "break point converted", "takes the break", "double break", "holds serve easily"]):
        return {
            "market": "Set Winner",
            "confidence": 82,
            "reason": "Break advantage or control language detected"
        }

    elif any(kw in text for kw in ["dictating every point", "controlling rallies", "dominant first serve", "barely missing", "storming through"]):
        return {
            "market": "Set Winner",
            "confidence": 79,
            "reason": "Consistent momentum language detected"
        }

    elif any(kw in text for kw in ["tight game", "on serve", "nothing in it", "evenly matched"]):
        return {
            "market": "Set Winner",
            "confidence": 67,
            "reason": "Tight contest, but stable performance edge"
        }

    elif any(kw in text for kw in ["won last 3 games", "swing in momentum", "flipped the script", "turned the tide"]):
        return {
            "market": "Set Winner",
            "confidence": 75,
            "reason": "Momentum reversal tone"
        }

    return None  # No clear signal