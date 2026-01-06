import feedparser
from src.settings import RSS_FEEDS, KEYWORDS

def get_news_briefing(limit_per_feed=3):
    """
    Fetches news from RSS, filters by keywords, and returns a structured list.
    """
    articles = []
    
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            source_name = feed.feed.get('title', 'Unknown Source')
            
            for entry in feed.entries[:limit_per_feed]:
                title = entry.get('title', '')
                link = entry.get('link', '')
                summary = entry.get('summary', '')

                # Simple scoring: +1 point for every keyword found in title
                score = 0
                for kw in KEYWORDS:
                    if kw.lower() in title.lower():
                        score += 1
                
                articles.append({
                    "source": source_name,
                    "title": title,
                    "link": link,
                    "summary": summary[:150] + "...", # Truncate long summaries
                    "score": score
                })
        except Exception as e:
            print(f"⚠️ Error parsing {url}: {e}")
            continue
    
    # Sort by score (relevance) then return top 10
    articles.sort(key=lambda x: x['score'], reverse=True)
    return articles[:10]
