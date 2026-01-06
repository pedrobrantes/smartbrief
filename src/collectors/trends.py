import feedparser

def get_google_trends(geo="BR"):
    """
    Fetches Daily Search Trends via RSS from Google.
    Returns the top 5 trending topics.
    """
    # RSS URL for Daily Search Trends
    rss_url = f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={geo}"
    
    trends = []
    try:
        feed = feedparser.parse(rss_url)
        
        for entry in feed.entries[:5]:
            # Google Trends RSS structure puts traffic in 'ht_approx_traffic'
            traffic = entry.get('ht_approx_traffic', 'N/A')
            
            trends.append({
                "title": entry.title,
                "traffic": traffic,
                "link": entry.link,
                "pubDate": entry.published
            })
    except Exception as e:
        print(f"⚠️ Error fetching Trends: {e}")
        
    return trends
