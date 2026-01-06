import json
from google import genai
from google.genai import types
from src.settings import GEMINI_API_KEY

def generate_daily_report(market_data, news_data):
    """
    Uses Gemini (New SDK) to act as a Daily Editor.
    Generates: Market Summary, News Highlights, Word of the Day, and Trivia.
    """
    # Default structure in case of failure
    fallback = {
        "market_summary": "Data available below.",
        "news_summary": "Check the links below.",
        "word_of_day": {"word": "Error", "translation": "Erro", "definition": "AI Unavailable", "example": "-"},
        "trivia": "Did you know? APIs can fail sometimes.",
        "chart_config": {"show": True, "type": "bar"}
    }

    if not GEMINI_API_KEY:
        return fallback

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        # Prepare context
        market_str = "\n".join([f"- {i['name']}: {i['change']:.2f}%" for i in market_data])
        news_str = "\n".join([f"- [{i['source']}] {i['title']}" for i in news_data[:5]])

        prompt = f"""
        You are the Editor-in-Chief of "SmartBrief", a personal daily newsletter.
        
        INPUT DATA:
        Market:
        {market_str}
        
        Top Headlines:
        {news_str}

        TASK:
        Generate a JSON response with the following sections:
        1. "market_summary": A witty financial summary (max 40 words).
        2. "news_summary": A synthesized paragraph connecting the top stories (max 50 words).
        3. "word_of_day": A useful/sophisticated English word.
           - Fields: "word", "translation" (PT-BR), "definition" (English), "example" (sentence).
        4. "trivia": A random, interesting fact about science, history, or tech.
        5. "chart_config": Decide visualization.
           - "show": true/false
           - "type": "bar", "horizontalBar", or "doughnut"

        Ensure the JSON is valid.
        """

        response = client.models.generate_content(
            model='gemini-2.0-flash', # Or gemini-1.5-flash
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type='application/json'
            )
        )
        
        return json.loads(response.text)

    except Exception as e:
        print(f"❌ AI Error: {e}")
        return fallback
