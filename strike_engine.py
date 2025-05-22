
import re

def detect_market(phrase):
    phrase = phrase.lower()
    if 'first' in phrase:
        return "First Goalscorer"
    elif 'brace' in phrase or 'double' in phrase or 'two' in phrase:
        return "2+ Goalscorer"
    elif 'equalis' in phrase:
        return "Team to Score Next"
    elif 'winner' in phrase or 'seals' in phrase or 'clinches' in phrase:
        return "Last Goalscorer"
    else:
        return "Anytime Goalscorer"

def extract_player(text, phrase):
    words = text.split()
    for i, word in enumerate(words):
        if phrase.lower() in word.lower():
            window = words[max(i-5,0):i+6]
            names = [w for w in window if re.match(r'[A-Z][a-z]+', w)]
            if names:
                return " ".join(names[:2])
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
                market = detect_market(phrase)
                strikes.append({
                    "player": player,
                    "phrase": phrase,
                    "market": market,
                    "odds": 2.75,
                    "confidence": 70 + len(phrase) % 10
                })
                break

    return strikes
