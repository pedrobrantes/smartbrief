import sys
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# Path fix
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.settings import EMAIL_TO, CHART_THEME
from src.collectors.finance import get_market_data
from src.visualizers.charts import generate_chart_url
from src.agents.analyst import generate_market_report # Changed import name
from src.core.mailer import send_email

def main():
    print("🚀 Starting SmartBrief Agent...")

    # 1. Extract
    print("📥 Collecting data...")
    market_data = get_market_data()
    if not market_data:
        print("❌ No data. Aborting.")
        return

    # 2. Agent Decision (The Brain)
    print("🧠 Agent is thinking...")
    report = generate_market_report(market_data)
    
    summary_text = report.get("summary", "No summary.")
    chart_decision = report.get("chart_type", "bar")
    should_show_chart = report.get("show_chart", True)

    print(f"💡 Agent decided: Chart='{chart_decision}'")

    # 3. Load / Visualize (Conditional)
    chart_url = None
    if should_show_chart and chart_decision != "none":
        print(f"🎨 Generating {chart_decision} chart...")
        chart_url = generate_chart_url(market_data, chart_type=chart_decision)

    # 4. Render
    print("📝 Rendering...")
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
    print(f"📨 Sending to {EMAIL_TO}...")
    try:
        result = send_email(EMAIL_TO, "SmartBrief: AI Report", html_content)
        print(f"✅ Success! ID: {result.get('id')}")
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    main()
