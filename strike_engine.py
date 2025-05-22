
import re

def extract_player(text, phrase):
    # Basic method: look for capitalized names near the phrase
    words = text.split()
    for i, word in enumerate(words):
        if phrase.lower() in word.lower():
            # look back and forward 5 words
            window = words[max(i-5,0):i+6]
            names = [w for w in window if re.match(r'[A-Z][a-z]+', w)]
            if names:
                return " ".join(names[:2])  # return best guess
    return "Unknown"

def generate_strikes(entries, phrases):
    strikes = []

    for entry in entries:
        text = (
            (entry.get("title") or "") + " " +
            (entry.get("summary") or "") + " " +
            (entry.get("description") or "")
        ).lower()

        full_text = (
            (entry.get("title") or "") + " " +
            (entry.get("summary") or "") + " " +
            (entry.get("description") or "")
        )

        for phrase in phrases:
            if phrase.lower() in text:
                player = extract_player(full_text, phrase)
                strikes.append({
                    "player": player,
                    "phrase": phrase,
                    "market": "Anytime Goalscorer",
                    "odds": 2.75,
                    "confidence": 70 + len(phrase) % 10
                })
                break

    return strikes
