import sys
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from mjml import mjml_to_html

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.settings import EMAIL_TO, CHART_THEME
from src.collectors.finance import get_market_data
from src.collectors.news import get_news_briefing
from src.collectors.trends import get_google_trends
from src.visualizers.charts import generate_sparkline_url, generate_chart_url
from src.agents.analyst import generate_daily_report
from src.core.mailer import send_email

def main():
    print("🚀 Starting SmartBrief OS...")

    print("📥 Collecting Data...")
    market_data = get_market_data()
    news_data = get_news_briefing()
    trends_data = get_google_trends(geo="BR")

    print("🎨 Generating Sparklines...")
    for item in market_data:
        item['sparkline'] = generate_sparkline_url(
            item.get('history', []), 
            item['change'] >= 0
        )

    print("🧠 Editor-in-Chief is working...")
    report = generate_daily_report(market_data, news_data)
    
    # Extract AI decisions
    chart_conf = report.get("chart_config", {})
    
    # Generate Main Chart (if AI requested)
    main_chart_url = None
    if chart_conf.get("show"):
        print(f"🎨 Generating {chart_conf.get('type')} chart...")
        main_chart_url = generate_chart_url(market_data, chart_type=chart_conf.get('type', 'bar'))

    print("📝 Compiling MJML...")
    env = Environment(loader=FileSystemLoader('src/templates'))
    template = env.get_template('email.mjml')
    
    rendered_mjml = template.render(
        title="Daily Briefing",
        date=datetime.now().strftime("%B %d, %Y"),
        market_items=market_data,
        news_items=news_data,
        trends=trends_data,
        palette=CHART_THEME,
        chart_url=main_chart_url,
        market_summary=report.get("market_summary", "No data."),
        news_summary=report.get("news_summary", "No data."),
        word=report.get("word_of_day", {}),
        trivia=report.get("trivia", "")
    )

    final_html = mjml_to_html(rendered_mjml)

    print(f"📨 Sending to {EMAIL_TO}...")
    try:
        send_email(EMAIL_TO, f"SmartBrief: {datetime.now().strftime('%d/%m')}", final_html.html)
        print("✅ Sent!")
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    main()
