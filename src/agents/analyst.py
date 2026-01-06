import json
import time
import random
from google import genai
from google.genai import types
from src.settings import GEMINI_API_KEY, GEMINI_MODELS_PRIORITY

def generate_daily_report(market_data, news_data):
    """
    Agent with Model Cascading.
    If the primary model hits a rate limit (429), it switches to the next model in the priority list.
    """
    fallback = {
        "market_summary": "Data available below (AI unavailable).",
        "news_summary": "Check the links below.",
        "word_of_day": {"word": "Persistence", "translation": "Persistência", "definition": "Firm continuance in a course of action.", "example": "Coding requires persistence."},
        "trivia": "Did you know? This report fell back to legacy logic.",
        "chart_config": {"show": True, "type": "bar"}
    }

    if not GEMINI_API_KEY:
        return fallback

    client = genai.Client(api_key=GEMINI_API_KEY)

    market_str = "\n".join([f"- {i['name']}: {i['change']:.2f}%" for i in market_data])
    news_str = "\n".join([f"- [{i['source']}] {i['title']}" for i in news_data[:5]])

    prompt = f"""
    You are the Editor-in-Chief of "SmartBrief".
    
    INPUT DATA:
    Market:
    {market_str}
    Top Headlines:
    {news_str}

    TASK:
    Generate a JSON response with:
    1. "market_summary": Witty financial summary (max 40 words).
    2. "news_summary": Synthesized paragraph connecting stories (max 50 words).
    3. "word_of_day": Useful English word. Fields: "word", "translation" (PT-BR), "definition", "example".
    4. "trivia": Interesting fact.
    5. "chart_config": {{"show": true, "type": "bar"|"horizontalBar"|"doughnut"}}

    Output strictly valid JSON.
    """

    # --- MODEL CASCADING LOGIC ---
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
            error_msg = str(e)
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                print(f"   ⚠️ Rate Limit on {model_name}. Switching...")
                time.sleep(1) # Brief pause before next model
                continue # Try next model in list
            elif "404" in error_msg:
                print(f"   ⚠️ Model {model_name} not found. Switching...")
                continue
            else:
                print(f"   ❌ Critical AI Error ({model_name}): {e}")
                # If it's not a rate limit, it might be a prompt issue, so we stop to save time
                break
    
    print("❌ All AI models failed. Using fallback.")
    return fallback
