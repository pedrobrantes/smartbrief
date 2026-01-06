import feedparser
import requests

def get_google_trends(geo="BR"):
    """
    Busca o RSS do Google Trends fingindo ser um navegador.
    """
    rss_url = f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={geo}"
    
    trends = []
    try:
        # TRUQUE: User-Agent para evitar bloqueio 429/403 do Google
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(rss_url, headers=headers, timeout=10)
        
        # Parseia o conteúdo baixado
        feed = feedparser.parse(response.content)
        
        for entry in feed.entries[:5]:
            # Tenta pegar o tráfego, se não existir, põe um valor padrão
            traffic = entry.get('ht_approx_traffic', 'Hot')
            
            trends.append({
                "title": entry.title,
                "traffic": traffic,
                "link": entry.link
            })
    except Exception as e:
        print(f"⚠️ Erro no Trends: {e}")
        # Dados falsos para não quebrar o layout se falhar
        return [{"title": "Erro ao buscar Trends", "traffic": "0", "link": "#"}]
        
    return trends
