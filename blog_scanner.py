# blog_scanner.py

import feedparser
import re
from lang_detect import detect_language_and_translate

def fetch_blog_entries(feed_url):
    try:
        feed = feedparser.parse(feed_url)
        entries = []

        for entry in feed.entries[:10]:
            raw_text = entry.get("title", "") + " " + entry.get("description", "")
            cleaned = clean_text(raw_text)
            translated = detect_language_and_translate(cleaned)
            entries.append(translated)

        return entries

    except Exception as e:
        print(f"[Blog Scanner] Error fetching feed: {e}")
        return []

def clean_text(text):
    # Basic blog text cleaner
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML
    text = re.sub(r'\s+', ' ', text)     # Collapse whitespace
    return text.strip()