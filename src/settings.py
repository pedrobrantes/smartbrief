import os
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
EMAIL_TO = os.getenv("EMAIL_TO")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODELS_PRIORITY = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]

TICKERS = ["USDBRL=X", "BTC-USD", "PETR4.SA", "VALE3.SA", "MXRF11.SA"]
RSS_FEEDS = ["https://g1.globo.com/rss/g1/", "https://feeds.bbci.co.uk/news/rss.xml"]
KEYWORDS = ["Artificial Intelligence", "Linux", "Rust", "Crypto", "Startup Brazil"]

CHART_THEME = {
    "bg": "#FDF8F5",
    "card": "#FFFFFF",
    "primary": "795548",
    "gain": "2E7D32",
    "loss": "C62828",
    "accent": "E65100",
    "muted": "999999"
}

def _icon(name, color_key):
    color = CHART_THEME.get(color_key, CHART_THEME['primary'])
    return f"https://img.icons8.com/material-sharp/48/{color}/{name}.png"

ICONS = {
    "market": _icon("line-chart", "primary"),
    "news": _icon("news", "primary"),
    "trending": _icon("fire", "accent"),
    "word": _icon("bookmark", "primary"),
    "trivia": _icon("idea", "accent"),
    "arrow_up": _icon("filled-sent", "gain"),
    "arrow_down": _icon("filled-sent", "loss"),
    "link": _icon("external-link", "muted")
}
