import feedparser
import requests

def get_google_trends(geo="BR"):
    """
    Fetches Google Trends using the Atom Feed endpoint (pn=p42 for Brazil).
    This endpoint is often more stable for scripts than the Daily RSS.
    """
    # p42 = Brazil index in Google Trends Atom
    url = "https://trends.google.com/trends/hottrends/atom/feed?pn=p42"
    
    trends = []
    try:
        # Standard headers
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"⚠️ Google Trends blocked/failed: Status {response.status_code}")
            return []

        feed = feedparser.parse(response.content)
        
        for entry in feed.entries[:5]:
            # Atom feeds usually put the approx traffic in the content or summary
            # We will default to "Trending" if specific data isn't parseable
            traffic = "Hot"
            
            # Try to find traffic number in standard extensions
            if hasattr(entry, 'ht_approx_traffic'):
                traffic = entry.ht_approx_traffic
            
            trends.append({
                "title": entry.title,
                "traffic": traffic,
                "link": entry.link
            })

    except Exception as e:
        print(f"❌ Trends Collector Error: {e}")
        return []
        
    return trends
