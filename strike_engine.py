
def generate_strikes(entries, phrases):
    strikes = []

    for entry in entries:
        text = (
            (entry.get("title") or "") + " " +
            (entry.get("summary") or "") + " " +
            (entry.get("description") or "")
        ).lower()

        for phrase in phrases:
            if phrase.lower() in text:
                strikes.append({
                    "player": phrase.title(),
                    "market": "Anytime Goalscorer",
                    "odds": 2.75,
                    "confidence": 70 + len(phrase) % 10
                })
                break

    return strikes
