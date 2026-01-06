import feedparser
import urllib.parse
from datetime import datetime
from time import mktime
from src.settings import RSS_FEEDS, KEYWORDS

def get_news_briefing():
    """
    Aggregates news from two sources:
    1. General Feeds (Static RSS defined in settings).
    2. Active Search (Google News RSS for each Keyword).
    """
    articles = []
    seen_links = set()

    print(f"   ↳ 🔍 Searching for specific topics: {', '.join(KEYWORDS)}...")

    # 1. Active Keyword Search (Google News)
    for keyword in KEYWORDS:
        # Construct dynamic query for last 24h (when:1d) to ensure recency
        encoded_kw = urllib.parse.quote(keyword)
        search_url = f"https://news.google.com/rss/search?q={encoded_kw}+when:1d&hl=pt-BR&gl=BR&ceid=BR:pt-419"
        
        _fetch_and_parse(search_url, articles, seen_links, limit=2, source_tag=f"Topic: {keyword}")

    # 2. General World News (Static Feeds)
    print(f"   ↳ 🌍 Fetching general headlines...")
    for url in RSS_FEEDS:
        _fetch_and_parse(url, articles, seen_links, limit=3, source_tag="General")

    # Sort by date (newest first)
    # feedparser uses 'published_parsed' (struct_time). We handle None cases safely.
    articles.sort(key=lambda x: x.get('timestamp', 0), reverse=True)

    return articles[:12] # Return top 12 mixed results

def _fetch_and_parse(url, articles_list, seen_set, limit=3, source_tag=""):
    try:
        feed = feedparser.parse(url)
        # Use feed title if available, otherwise use the tag
        feed_title = feed.feed.get('title', source_tag)
        
        count = 0
        for entry in feed.entries:
            if count >= limit:
                break
            
            link = entry.get('link', '')
            
            # Deduplication check
            if link in seen_set:
                continue
            
            # Parse Date
            published_parsed = entry.get('published_parsed')
            timestamp = mktime(published_parsed) if published_parsed else 0
            
            articles_list.append({
                "source": feed_title,
                "title": entry.get('title', 'No Title'),
                "link": link,
                "summary": _clean_summary(entry.get('summary', '')),
                "timestamp": timestamp,
                "tag": source_tag # Useful for the UI to show why this news is here
            })
            
            seen_set.add(link)
            count += 1
            
    except Exception as e:
        print(f"⚠️ Error fetching {url}: {e}")

def _clean_summary(summary):
    # Basic HTML tag removal if needed, or truncation
    # Google News summaries are often HTML heavy; simple text is safer for email
    return summary.split('<')[0][:150] + "..." if summary else ""
