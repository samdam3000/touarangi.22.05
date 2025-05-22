# correct_score.py

def evaluate_correct_score_tennis(blog_text):
    """
    Analyzes blog text to predict likely correct score outcomes for a tennis set.
    Returns a prediction dict with score and confidence if a match is found.
    """

    text = blog_text.lower()

    if any(kw in text for kw in ["he’s folding", "she’s done", "dominating", "no resistance", "steamrolling"]):
        return {
            "score_prediction": "6-1",
            "confidence": 83,
            "reason": "Collapse tone detected (folding/resistance gone)"
        }

    elif any(kw in text for kw in ["tight battle", "trading blows", "evenly matched", "neck and neck", "both players locked in"]):
        return {
            "score_prediction": "7-5",
            "confidence": 78,
            "reason": "Close contest tone (tight match)"
        }

    elif any(kw in text for kw in ["one-way traffic", "no answer", "overwhelmed", "battering", "break after break"]):
        return {
            "score_prediction": "6-2",
            "confidence": 81,
            "reason": "Dominance with moderate pushback"
        }

    elif any(kw in text for kw in ["broken early", "slow start", "bad opening", "quick 3-0", "can't hold serve"]):
        return {
            "score_prediction": "6-3",
            "confidence": 76,
            "reason": "Early break indicator, mild recovery"
        }

    return None  # No clear signal found