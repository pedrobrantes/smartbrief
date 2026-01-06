import sys
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from mjml import mjml_to_html

# Ensure the project root is in sys.path to resolve 'src' imports correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.settings import EMAIL_TO, CHART_THEME, ICONS
from src.collectors.finance import get_market_data
from src.collectors.news import get_news_briefing
from src.collectors.trends import get_google_trends
from src.visualizers.charts import generate_sparkline_url, generate_chart_url
from src.agents.analyst import generate_daily_report
from src.core.mailer import send_email

def main():
    print("🚀 Starting SmartBrief OS...")

    # 1. Data Collection
    print("📥 Collecting Finance Data...")
    market_data = get_market_data()
    
    print("📥 Collecting News Headlines...")
    news_data = get_news_briefing()

    print("📥 Collecting Google Trends...")
    trends_data = get_google_trends(geo="BR")

    # 2. Visual Asset Generation (Sparklines)
    print("🎨 Generating Sparklines...")
    for item in market_data:
        # Generate a mini-chart URL for each asset and inject it into the item dict
        item['sparkline'] = generate_sparkline_url(
            item.get('history', []), 
            item['change'] >= 0
        )

    # 3. AI Processing (Editor-in-Chief)
    print("🧠 Editor-in-Chief is analyzing...")
    report = generate_daily_report(market_data, news_data)
    
    # 4. Main Chart Generation (Conditional)
    chart_conf = report.get("chart_config", {})
    main_chart_url = None
    
    if chart_conf.get("show"):
        print(f"🎨 Generating {chart_conf.get('type')} chart...")
        main_chart_url = generate_chart_url(
            market_data, 
            chart_type=chart_conf.get('type', 'bar')
        )

    # 5. Template Rendering (Jinja2 -> MJML -> HTML)
    print("📝 Compiling MJML Template...")
    env = Environment(loader=FileSystemLoader('src/templates'))
    template = env.get_template('email.mjml')
    
    # Render Jinja2 logic first
    rendered_mjml = template.render(
        title="Daily Briefing",
        date=datetime.now().strftime("%B %d, %Y"),
        market_items=market_data,
        news_items=news_data,
        trends=trends_data,
        palette=CHART_THEME,
        icons=ICONS,
        chart_url=main_chart_url,
        market_summary=report.get("market_summary", "No analysis available."),
        news_summary=report.get("news_summary", "No analysis available."),
        word=report.get("word_of_day", {}),
        trivia=report.get("trivia", "")
    )

    # Compile MJML to responsive HTML
    final_html = mjml_to_html(rendered_mjml)

    # 6. Email Delivery
    print(f"📨 Sending email to {EMAIL_TO}...")
    try:
        subject = f"SmartBrief: {datetime.now().strftime('%d/%m')}"
        result = send_email(EMAIL_TO, subject, final_html.html)
        print(f"✅ Email sent successfully! ID: {result.get('id')}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    main()
