import math
import yfinance as yf
from src.settings import TICKERS

def get_market_data():
    results = []
    
    # Map raw tickers to display names if needed, or use raw ticker as name
    # For simplicity, we are using the ticker itself as the name
    
    for ticker in TICKERS:
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="5d")
            
            if len(hist) >= 2:
                price_now = float(hist['Close'].iloc[-1])
                price_prev = float(hist['Close'].iloc[-2])
                
                if price_prev == 0:
                    change = 0.0
                else:
                    change = ((price_now - price_prev) / price_prev) * 100
                
                if math.isnan(change) or math.isinf(change):
                    change = 0.0
                if math.isnan(price_now) or math.isinf(price_now):
                    price_now = 0.0

                results.append({
                    "name": ticker,
                    "price": price_now,
                    "change": change
                })
        except Exception:
            continue

    return results
