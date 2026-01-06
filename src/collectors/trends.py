import feedparser
import requests
from src.collectors.news import get_news_briefing # Fallback import

def get_google_trends(geo="BR"):
    # URL oficial do Daily Trends RSS
    url = f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={geo}"
    
    try:
        # 1. HEAVY ARMOR: Headers + Cookies to bypass Google Bot Detection
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache"
        }
        
        # Cookies mágicos para pular a tela de "Antes de continuar"
        cookies = {
            "NID": "511=Ocj1...", # Cookie genérico
            "CONSENT": "YES+CB.20210720-08-p0.en+FX+410" # Simula aceite de termos
        }
        
        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        
        # 2. Check for Blocking
        if response.status_code != 200:
            return [{
                "title": f"Google Blocked: {response.status_code}",
                "traffic": "Error",
                "link": "https://trends.google.com"
            }]

        # 3. Parse RSS
        feed = feedparser.parse(response.content)
        
        trends = []
        if not feed.entries:
            # Se baixou 200 OK mas não tem entradas, provavelmente é página de Captcha
            return [{"title": "Google Captcha Block", "traffic": "Bot Detected", "link": "#"}]

        for entry in feed.entries[:5]:
            # Namespace handling robusto
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
        # Se explodir (ex: sem internet), retorna o erro visível
        return [{
            "title": f"Sys Error: {str(e)[:20]}", 
            "traffic": "Fail", 
            "link": "#"
        }]
