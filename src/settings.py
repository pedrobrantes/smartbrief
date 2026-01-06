import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

# API Keys
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
EMAIL_TO = os.getenv("EMAIL_TO")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# AI Configuration
GEMINI_MODELS_PRIORITY = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]

# 1. Finance Config
TICKERS = ["USDBRL=X", "BTC-USD", "PETR4.SA", "VALE3.SA", "MXRF11.SA"]

# 2. General News Sources
RSS_FEEDS = ["https://g1.globo.com/rss/g1/", "https://feeds.bbci.co.uk/news/rss.xml"]

# 3. Active Search Targets
KEYWORDS = ["Artificial Intelligence", "Linux", "Rust", "Crypto", "Startup Brazil"]

# 4. Visual Palette
CHART_THEME = {
    "bg": "#FDF8F5",
    "card": "#FFFFFF",
    "primary": "#795548",
    "text": "#3E2723",
    "gain": "#2E7D32",
    "loss": "#C62828",
    "grid": "rgba(62, 39, 35, 0.1)"
}

# --- FIXED ICON SYSTEM ---
def _get_icon_url(collection, name, color):
    # Fix: Encode color explicitly without using 'urllib' for the whole string
    # Fix: Use '/' instead of ':' in the URL path for better email compatibility
    clean_color = color.replace("#", "%23")
    return f"https://api.iconify.design/{collection}/{name}.png?color={clean_color}&height=24&width=24"

# Usando Phosphor Icons (ph) com barras
ICONS = {
    "market": _get_icon_url("ph", "chart-line-up-bold", CHART_THEME['primary']),
    "news": _get_icon_url("ph", "newspaper-bold", CHART_THEME['primary']),
    "trending": _get_icon_url("ph", "fire-bold", "#E65100"),
    "word": _get_icon_url("ph", "book-bookmark-bold", CHART_THEME['primary']),
    "trivia": _get_icon_url("ph", "lightbulb-bold", "#FBC02D"),
    "arrow_up": _get_icon_url("ph", "arrow-up-right-bold", CHART_THEME['gain']),
    "arrow_down": _get_icon_url("ph", "arrow-down-right-bold", CHART_THEME['loss']),
    "link": _get_icon_url("ph", "arrow-square-out-bold", "#999999")
}
