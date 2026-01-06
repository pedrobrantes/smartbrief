import os
import urllib.parse
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
    "primary": "#795548",
    "text": "#3E2723",
    "gain": "#2E7D32",
    "loss": "#C62828",
    "grid": "rgba(62, 39, 35, 0.1)"
}

def _get_icon_url(name, color):
    clean_color = color.replace("#", "%23")
    return f"https://quickchart.io/chart/render/icon?icon=mdi:{name}&color={clean_color}&size=32&format=png"

ICONS = {
    "market": _get_icon_url("chart-line", CHART_THEME['primary']),
    "news": _get_icon_url("newspaper-variant-outline", CHART_THEME['primary']),
    "trending": _get_icon_url("fire", "#E65100"),
    "word": _get_icon_url("bookmark-outline", CHART_THEME['primary']),
    "trivia": _get_icon_url("lightbulb-on-outline", "#FBC02D"),
    "arrow_up": _get_icon_url("arrow-top-right", CHART_THEME['gain']),
    "arrow_down": _get_icon_url("arrow-bottom-right", CHART_THEME['loss']),
    "link": _get_icon_url("open-in-new", "#999999")
}
