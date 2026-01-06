import os
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
EMAIL_TO = os.getenv("EMAIL_TO")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

TICKERS = [
    "USDBRL=X",
    "BTC-USD",
    "PETR4.SA",
    "VALE3.SA",
    "MXRF11.SA"
]

CHART_THEME = {
    "bg": "#FDF8F5",
    "card": "#FFFFFF",
    "primary": "#795548",
    "text": "#3E2723",
    "gain": "#66BB6A",
    "loss": "#EF5350",
    "grid": "rgba(62, 39, 35, 0.1)"
}
