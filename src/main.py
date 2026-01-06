import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

from src.settings import EMAIL_TO, CHART_THEME
from src.collectors.finance import get_market_data
from src.visualizers.charts import generate_chart_url
from src.agents.analyst import generate_market_summary
from src.core.mailer import send_email

def main():
    print("🚀 Starting SmartBrief...")

    # 1. Extract
    print("📥 Collecting financial data...")
    market_data = get_market_data()
    if not market_data:
        print("❌ No data collected. Aborting.")
        return

    # 2. Transform & Analyze
    print("🤖 Generating analysis...")
    summary_text = generate_market_summary(market_data)

    # 3. Load / Visualize
    print("🎨 Generating chart...")
    chart_url = generate_chart_url(market_data)

    # 4. Render Template
    print("📝 Rendering HTML...")
    env = Environment(loader=FileSystemLoader('src/templates'))
    template = env.get_template('email.html')
    
    html_content = template.render(
        title="SmartBrief Daily",
        date=datetime.now().strftime("%B %d, %Y"),
        items=market_data,
        chart_url=chart_url,
        palette=CHART_THEME,
        ai_summary=summary_text
    )

    # 5. Send
    print(f"📨 Sending email to {EMAIL_TO}...")
    try:
        result = send_email(EMAIL_TO, "SmartBrief: Market Update", html_content)
        print(f"✅ Success! ID: {result.get('id')}")
    except Exception as e:
        print(f"❌ Delivery failed: {e}")

if __name__ == "__main__":
    main()
