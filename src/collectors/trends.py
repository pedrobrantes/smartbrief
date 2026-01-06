import feedparser
import requests

def get_google_trends(geo="BR"):
    """
    Attempts multiple Google Trends endpoints to find a working one.
    """
    # Strategy: Try endpoints in order
    urls = [
        # 1. Daily Trends (Standard)
        f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={geo}",
        # 2. Realtime Trends (Backup)
        f"https://trends.google.com/trends/trendingsearches/realtime/rss?geo={geo}&category=all"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/rss+xml, application/xml, text/xml"
    }

    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
                if feed.entries:
                    return _parse_feed(feed)
            
            # If 404 or empty, just continue to next URL
            
        except Exception:
            continue
            
    # If all fail, return empty list (cleaner than showing an error in UI)
    print("⚠️ All Google Trends endpoints failed.")
    return []

def _parse_feed(feed):
    trends = []
    for entry in feed.entries[:5]:
        # Handle traffic namespace
        traffic = "Trending"
        if hasattr(entry, 'ht_approx_traffic'):
            traffic = entry.ht_approx_traffic
        
        trends.append({
            "title": entry.title,
            "traffic": traffic,
            "link": entry.link
        })
    return trends
