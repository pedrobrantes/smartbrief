import feedparser
import requests

def get_google_trends(geo="BR"):
    rss_url = f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={geo}"
    
    trends = []
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(rss_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return []

        feed = feedparser.parse(response.content)
        
        for entry in feed.entries[:5]:
            traffic = getattr(entry, 'ht_approx_traffic', 'Hot')
            
            trends.append({
                "title": entry.title,
                "traffic": traffic,
                "link": entry.link
            })
    except Exception as e:
        print(f"⚠️ Trends error: {e}")
        return []
        
    return trends
