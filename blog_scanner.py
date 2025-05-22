import feedparser

def fetch_blog_entries(feed_url):
    feed = feedparser.parse(feed_url)
    return feed.entries[:30]  # increased from 10 to 30