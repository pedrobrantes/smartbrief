import sys
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# Path fix
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.settings import EMAIL_TO, CHART_THEME
from src.collectors.finance import get_market_data
from src.collectors.news import get_news_briefing
from src.visualizers.charts import generate_chart_url
from src.agents.analyst import generate_daily_report
from src.core.mailer import send_email

def main():
    print("🚀 Starting SmartBrief OS...")

    # 1. Collect Data (Parallelizable in future)
    print("📥 Collecting Finance...")
    market_data = get_market_data()
    
    print("📥 Collecting News...")
    news_data = get_news_briefing()

    # 2. AI Processing
    print("🧠 Editor-in-Chief is working...")
    report = generate_daily_report(market_data, news_data)
    
    # Extract AI decisions
    market_summary = report.get("market_summary", "")
    news_summary = report.get("news_summary", "")
    word_data = report.get("word_of_day", {})
    trivia = report.get("trivia", "")
    chart_conf = report.get("chart_config", {})

    # 3. Visualization
    chart_url = None
    if chart_conf.get("show"):
        print(f"🎨 Generating {chart_conf.get('type')} chart...")
        chart_url = generate_chart_url(market_data, chart_type=chart_conf.get('type', 'bar'))

    # 4. Render
    print("📝 Rendering HTML...")
    env = Environment(loader=FileSystemLoader('src/templates'))
    template = env.get_template('email.html')
    
    html_content = template.render(
        title="Daily Briefing",
        date=datetime.now().strftime("%B %d, %Y"),
        market_items=market_data,
        news_items=news_data,
        chart_url=chart_url,
        palette=CHART_THEME,
        # AI Content
        market_summary=market_summary,
        news_summary=news_summary,
        word=word_data,
        trivia=trivia
    )

    # 5. Send
    print(f"📨 Sending to {EMAIL_TO}...")
    try:
        send_email(EMAIL_TO, f"Briefing: {datetime.now().strftime('%d/%m')}", html_content)
        print("✅ Sent!")
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    main()
