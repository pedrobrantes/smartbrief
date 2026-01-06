import json
import time
from google import genai
from google.genai import types
from src.settings import GEMINI_API_KEY, GEMINI_MODELS_PRIORITY

def generate_daily_report(market_data, news_data):
    fallback = {
        "market_summary": "Market data analyzed. Check details below.",
        "news_summary": "Top headlines synthesized. Links available.",
        "word_of_day": {
            "word": "Resilience", 
            "translation": "Resiliência", 
            "definition": "The capacity to recover quickly from difficulties.", 
            "example": "The system showed resilience by switching models."
        },
        "trivia": "AI models can sometimes be overloaded during peak hours.",
        "chart_config": {"show": True, "type": "bar"}
    }

    if not GEMINI_API_KEY:
        return fallback

    client = genai.Client(api_key=GEMINI_API_KEY)

    market_str = "\n".join([f"- {i['name']}: {i['change']:.2f}%" for i in market_data])
    news_str = "\n".join([f"- [{i['source']}] {i['title']}" for i in news_data[:5]])

    prompt = f"""
    You are the Editor-in-Chief of "SmartBrief".
    
    DATA:
    Market: {market_str}
    News: {news_str}

    TASK:
    Generate JSON:
    1. "market_summary": Witty summary (40 words).
    2. "news_summary": Synthesized news (50 words).
    3. "word_of_day": "word", "translation", "definition", "example".
    4. "trivia": Interesting fact.
    5. "chart_config": {{"show": true, "type": "bar"}}
    """

    for model_name in GEMINI_MODELS_PRIORITY:
        try:
            print(f"   ↳ 🧠 Trying model: {model_name}...")
            
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type='application/json'
                )
            )
            return json.loads(response.text)

        except Exception as e:
            err = str(e).upper()
            # Catch 429 (Rate Limit), 503 (Overloaded), 500 (Internal), 404 (Missing)
            if any(code in err for code in ["429", "503", "500", "404", "RESOURCE_EXHAUSTED", "UNAVAILABLE"]):
                print(f"   ⚠️ {model_name} unavailable ({err[:15]}...). Switching...")
                time.sleep(1)
                continue
            else:
                print(f"   ❌ Fatal Error on {model_name}: {e}")
                break
    
    print("❌ All AI models failed. Using fallback.")
    return fallback
