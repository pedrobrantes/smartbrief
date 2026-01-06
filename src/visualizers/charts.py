import requests
from src.settings import CHART_THEME

def generate_chart_url(data, chart_type="bar"):
    if not data or chart_type == "none":
        return None

    labels = [d['name'] for d in data]
    values = [d['change'] for d in data]
    colors = [CHART_THEME['gain'] if v >= 0 else CHART_THEME['loss'] for v in values]

    # Base configuration
    config = {
        "type": chart_type,
        "data": {
            "labels": labels,
            "datasets": [{
                "data": values,
                "backgroundColor": colors,
                "borderRadius": 20,
                "borderSkipped": False
            }]
        },
        "options": {
            "legend": {"display": False},
            "scales": {
                "yAxes": [{"display": False}],
                "xAxes": [{"display": False}]
            }
        }
    }

    # Specific overrides based on type
    if chart_type == "horizontalBar":
        config["options"]["scales"] = {"xAxes": [{"display": False}], "yAxes": [{"display": True}]}
        config["data"]["datasets"][0]["barThickness"] = 15
    elif chart_type == "doughnut":
        config["options"]["scales"] = {"xAxes": [{"display": False}], "yAxes": [{"display": False}]}
        config["options"]["cutoutPercentage"] = 50

    try:
        response = requests.post(
            "https://quickchart.io/chart/create",
            json={
                "chart": config,
                "width": 500,
                "height": 200, # Increased height slightly
                "backgroundColor": "white",
                "format": "png",
                "version": "2"
            },
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get('url')
    except Exception:
        return None
    
    return None
