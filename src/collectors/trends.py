import feedparser
import requests

def get_google_trends(geo="BR"):
    # Official RSS Feed for Daily Search Trends
    url = f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={geo}"
    
    trends = []
    try:
        # 1. Masquerade as a real browser (Chrome 120)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.google.com/"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        # Debug: Print status if it fails
        if response.status_code != 200:
            print(f"⚠️ Google Trends blocked the request: Status {response.status_code}")
            return _fallback_trends()

        # 2. Parse XML
        feed = feedparser.parse(response.content)
        
        if not feed.entries:
            print("⚠️ Trends RSS retrieved but empty (parsing issue).")
            return _fallback_trends()

        for entry in feed.entries[:5]:
            # 3. Robust Namespace Handling
            # Feedparser might map 'ht:approx_traffic' to different attributes depending on version
            traffic = "Trending"
            
            if hasattr(entry, 'ht_approx_traffic'):
                traffic = entry.ht_approx_traffic
            elif hasattr(entry, 'ht_approxtraffic'):
                traffic = entry.ht_approxtraffic
            elif 'ht_approx_traffic' in entry:
                traffic = entry['ht_approx_traffic']
            
            trends.append({
                "title": entry.title,
                "traffic": traffic,
                "link": entry.link
            })

    except Exception as e:
        print(f"❌ Trends Collector Error: {e}")
        return _fallback_trends()
        
    return trends

def _fallback_trends():
    """Returns placeholder data so the email UI remains stable."""
    return [
        {"title": "Google Trends (API Blocked)", "traffic": "N/A", "link": "https://trends.google.com"},
        {"title": "Check Server Logs", "traffic": "N/A", "link": "#"}
    ]
