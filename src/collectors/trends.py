import feedparser
import requests
import urllib.parse
from src.settings import KEYWORDS

def get_google_trends(geo="BR"):
    url = f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={geo}"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "no-cache"
        }
        
        cookies = {"CONSENT": "YES+CB.20210720-08-p0.en+FX+410"}
        
        response = requests.get(url, headers=headers, cookies=cookies, timeout=5)
        
        # Se o Google bloquear (429/404/503) ou retornar algo que não é XML
        if response.status_code != 200 or b'<rss' not in response.content:
            print(f"⚠️ Google Trends unavailable ({response.status_code}). Using Fallback.")
            return _get_fallback_trends()

        feed = feedparser.parse(response.content)
        
        trends = []
        if not feed.entries:
            return _get_fallback_trends()

        for entry in feed.entries[:5]:
            traffic = "Hot"
            if hasattr(entry, 'ht_approx_traffic'):
                traffic = entry.ht_approx_traffic
            
            trends.append({
                "title": entry.title,
                "traffic": traffic,
                "link": entry.link
            })
            
        return trends

    except Exception as e:
        print(f"❌ Trends Error: {e}")
        return _get_fallback_trends()

def _get_fallback_trends():
    """
    Gera uma lista de trends baseada nas KEYWORDS do usuário.
    Isso garante que a UI nunca quebre ou mostre erros.
    """
    fallback = []
    # Pega as primeiras 5 keywords definidas no settings.py
    for kw in KEYWORDS[:5]:
        encoded_kw = urllib.parse.quote(kw)
        fallback.append({
            "title": kw,
            "traffic": "Interest", # Mostra que é um tópico de interesse
            "link": f"https://news.google.com/search?q={encoded_kw}"
        })
    return fallback
