import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
EMAIL_TO = os.getenv("EMAIL_TO")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# AI Configuration: Priority List (Cascade Strategy)
# 1. Try 2.5 Flash (Newest, Fast)
# 2. Try 2.0 Flash (Stable)
# 3. Try 1.5 Flash (Oldest, Highest Limits/Reliability)
GEMINI_MODELS_PRIORITY = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash"
]

# 1. Finance Config
TICKERS = [
    "USDBRL=X", "BTC-USD", "PETR4.SA", "VALE3.SA", "MXRF11.SA"
]

# 2. General News Sources
RSS_FEEDS = [
    "https://g1.globo.com/rss/g1/",
    "https://feeds.bbci.co.uk/news/rss.xml",
]

# 3. Active Search Targets
KEYWORDS = [
    "Artificial Intelligence", "Linux", "Rust Programming", "Crypto", 
    "Startup Brazil", "Data Analysis", "Software Engineering", "SQL", 
    "CyberSec", "NVIDEA", "Flamengo", "UFC", "Formula 1"
]

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
