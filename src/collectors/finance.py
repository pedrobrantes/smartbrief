import math
import yfinance as yf
from src.settings import TICKERS

def get_market_data():
    results = []
    
    try:
        # Fetch 7 days of history for sparklines
        tickers_str = " ".join(TICKERS)
        data = yf.download(tickers_str, period="7d", progress=False)['Close']
        
        for ticker in TICKERS:
            try:
                if len(TICKERS) > 1:
                    series = data[ticker].dropna()
                else:
                    series = data.dropna()

                if len(series) >= 2:
                    price_now = float(series.iloc[-1])
                    price_prev = float(series.iloc[-2])
                    
                    change = 0.0
                    if price_prev > 0:
                        change = ((price_now - price_prev) / price_prev) * 100
                    
                    history = [float(x) for x in series.tail(7).values.tolist()]

                    results.append({
                        "name": ticker.replace(".SA", "").replace("=X", ""),
                        "price": price_now,
                        "change": change,
                        "history": history
                    })
            except Exception as e:
                print(f"⚠️ Error processing {ticker}: {e}")
                continue

    except Exception as e:
        print(f"❌ yfinance fatal error: {e}")

    return results
