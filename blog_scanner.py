
import feedparser

BLOG_FEEDS = [
    "https://feeds.bbci.co.uk/sport/football/rss.xml?edition=uk",
    "https://www.espn.com/espn/rss/news",  # general sports
    "https://www.nrl.com/rss/news.xml",
    "https://www.skysports.com/rss/12040",  # football
    "https://www.skysports.com/rss/12016",  # rugby
    "https://www.skysports.com/rss/12118",  # cricket
    "https://www.skysports.com/rss/12025",  # boxing
    "https://www.sportingnews.com/us/rss",  # US-focused sport
    "https://www.reddit.com/r/nrl/.rss",    # NRL news (low priority backup)
]

def fetch_blog_entries():
    entries = []
    for url in BLOG_FEEDS:
        try:
            feed = feedparser.parse(url)
            entries.extend(feed.entries[:10])  # take 10 from each
        except Exception as e:
            print(f"[FEED ERROR] Failed to parse {url}: {e}")
    return entries[:50]  # cap to 50 entries total
