import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
EMAIL_TO = os.getenv("EMAIL_TO")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# AI Configuration
GEMINI_MODEL = "gemini-1.5-flash"  # Change to 'gemini-2.0-flash' if available/quota permits

# 1. Finance Config
TICKERS = [
    "USDBRL=X", "BTC-USD", "PETR4.SA", "VALE3.SA", "MXRF11.SA"
]

# 2. News Config (RSS Feeds)
RSS_FEEDS = [
    "https://g1.globo.com/rss/g1/",
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://techcrunch.com/feed/",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
]

# 3. Interest Keywords
KEYWORDS = ["AI", "Python", "NixOS", "Crypto", "Startup", "Brasil", "Innovation"]

# 4. Visual Styles
CHART_THEME = {
    "bg": "#FDF8F5",
    "card": "#FFFFFF",
    "primary": "#795548",
    "text": "#3E2723",
    "gain": "#66BB6A",
    "loss": "#EF5350",
    "grid": "rgba(62, 39, 35, 0.1)"
}
