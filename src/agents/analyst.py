def generate_market_summary(data):
    if not data:
        return "No market data available for analysis."

    gainers = [d for d in data if d['change'] > 0]
    losers = [d for d in data if d['change'] < 0]
    
    sentiment = "Neutral"
    if len(gainers) > len(losers):
        sentiment = "Bullish"
    elif len(losers) > len(gainers):
        sentiment = "Bearish"

    top_gainer = gainers[0]['name'] if gainers else 'None'
    top_loser = losers[0]['name'] if losers else 'None'

    summary = (
        f"The market sentiment is currently {sentiment}. "
        f"Top gainer: {top_gainer}. "
        f"Top loser: {top_loser}."
    )
    
    return summary
