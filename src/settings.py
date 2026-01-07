import os
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
EMAIL_TO = os.getenv("EMAIL_TO")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODELS_PRIORITY = [
    "gemini-2.5-flash", 
    "gemini-2.0-flash", 
    "gemini-3-flash", 
    "gemini-3-pro-preview", 
    "gemini-3-pro", 
    "gemini-1.5-flash", 
    "gemma-3-27b-it", 
    "gemini-2.0-flash-lite", 
    "gemini-flash-lite-latest", 
    "gemini-flash-latest", 
    "gemini-pro-latest"
]

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
    "muted": "999999",
    "white": "FFFFFF"
}

def _icon(name, color_key, size=96):
    color = CHART_THEME.get(color_key, CHART_THEME['primary'])
    clean_color = color.replace("#", "")
    return f"https://img.icons8.com/material-sharp/{size}/{clean_color}/{name}.png"

ICONS = {
    "market": _icon("line-chart", "primary"),
    "news": _icon("news", "primary"),
    "trending": _icon("hashtag", "primary"),
    "word": _icon("book", "white"),
    "trivia": _icon("light", "primary"),
    "arrow_up": _icon("long-arrow-up", "gain", size=48),
    "arrow_down": _icon("long-arrow-down", "loss", size=48),
    "link": _icon("external-link", "muted", size=48)
}
