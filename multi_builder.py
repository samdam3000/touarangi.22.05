# multi_builder.py

from datetime import datetime, timedelta

def detect_multi_opportunity(active_strikes, window=5):
    """
    Detects multi-strike combos within a given time window (default: 5 minutes).
    Returns a multi-strike recommendation if 2 or more valid strikes align.
    """
    now = datetime.utcnow()
    recent = [
        s for s in active_strikes
        if "confirmed_time" in s and (now - s["confirmed_time"]) <= timedelta(minutes=window)
    ]

    if len(recent) >= 2:
        # Prioritize strongest pair (by confidence)
        sorted_strikes = sorted(recent, key=lambda s: -s.get("confidence", 0))
        top_2 = sorted_strikes[:2]
        combined_conf = round(sum(s['confidence'] for s in top_2) / len(top_2), 2)

        return {
            "market": "Multi-Strike Combo",
            "legs": [s["player"] + " (" + s["market"] + ")" for s in top_2],
            "combined_confidence": combined_conf,
            "reason": "Multiple high-confidence triggers within window",
            "confirmed_time": now,
            "strike_type": "MULTI LOCK"
        }

    return None