import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

# ... (Previous API Keys) ...
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
EMAIL_TO = os.getenv("EMAIL_TO")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODELS_PRIORITY = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]

# ... (Configs for Tickers, RSS, Keywords remain the same) ...
TICKERS = ["USDBRL=X", "BTC-USD", "PETR4.SA", "VALE3.SA", "MXRF11.SA"]
RSS_FEEDS = ["https://g1.globo.com/rss/g1/", "https://feeds.bbci.co.uk/news/rss.xml"]
KEYWORDS = ["Artificial Intelligence", "Linux", "Rust", "Crypto", "Startup Brazil"]

# Visual Palette
CHART_THEME = {
    "bg": "#FDF8F5",
    "card": "#FFFFFF",
    "primary": "#795548", # Brown
    "text": "#3E2723",
    "gain": "#2E7D32",    # Darker Green for text/icons
    "loss": "#C62828",    # Darker Red for text/icons
    "grid": "rgba(62, 39, 35, 0.1)"
}

# --- NEW: ICON SYSTEM (Phosphor Icons via Iconify API) ---
# We encode the color to put it in the URL
def _get_icon_url(icon_name, color):
    safe_color = urllib.parse.quote(color)
    return f"https://api.iconify.design/ph:{icon_name}-bold.png?color={safe_color}&height=24"

ICONS = {
    "market": _get_icon_url("chart-line-up", CHART_THEME['primary']),
    "news": _get_icon_url("newspaper", CHART_THEME['primary']),
    "trending": _get_icon_url("fire", "#E65100"), # Orange for Fire
    "word": _get_icon_url("book-bookmark", CHART_THEME['primary']),
    "trivia": _get_icon_url("lightbulb", "#FBC02D"), # Yellow for Lightbulb
    "arrow_up": _get_icon_url("arrow-up-right", CHART_THEME['gain']),
    "arrow_down": _get_icon_url("arrow-down-right", CHART_THEME['loss']),
    "link": _get_icon_url("arrow-square-out", "#999999")
}
