import json
import google.generativeai as genai
from src.settings import GEMINI_API_KEY

def generate_market_report(data):
    """
    Returns a dictionary with 'summary', 'chart_type', and 'show_chart'.
    """
    if not data:
        return {"summary": "No data available.", "show_chart": False, "chart_type": "none"}

    if not GEMINI_API_KEY:
        return _fallback_report(data)

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')

        context_str = "\n".join([
            f"- {item['name']}: {item['change']:.2f}%" for item in data
        ])

        prompt = f"""
        You are an AI Editor for a financial newsletter.
        
        Market Data:
        {context_str}

        Task:
        1. Write a witty, professional summary (max 50 words).
        2. Decide if a chart is necessary to visualize this data.
        3. Choose the best chart type:
           - "bar": Good for comparing winners/losers.
           - "horizontalBar": Good if names are long or for ranking.
           - "doughnut": Good if data represents parts of a whole (rarely for price changes, but possible).
           - "none": If data is boring or unclear.

        Output strictly valid JSON:
        {{
            "summary": "Your text here",
            "show_chart": true/false,
            "chart_type": "bar" | "horizontalBar" | "doughnut" | "none"
        }}
        """

        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        return json.loads(response.text)

    except Exception as e:
        print(f"❌ AI Error: {e}")
        return _fallback_report(data)

def _fallback_report(data):
    return {
        "summary": "Market data processed (AI unavailable).",
        "show_chart": True,
        "chart_type": "bar"
    }
