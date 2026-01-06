import requests
from src.settings import CHART_THEME

def generate_chart_url(data, chart_type="bar"):
    if not data or chart_type == "none":
        return None

    labels = [d['name'] for d in data]
    values = [d['change'] for d in data]
    colors = [CHART_THEME['gain'] if v >= 0 else CHART_THEME['loss'] for v in values]

    config = {
        "type": chart_type,
        "data": {
            "labels": labels,
            "datasets": [{
                "data": values,
                "backgroundColor": colors,
                "borderRadius": 50,      # Pill shape
                "borderSkipped": False,  # Fully rounded
                "barThickness": 18,      # Thinner, more elegant bars
            }]
        },
        "options": {
            "devicePixelRatio": 2.0,     # HIGH RES (Retina Quality)
            "legend": {"display": False},
            "layout": {"padding": {"top": 10, "bottom": 10}}, # Space to breathe
            "scales": {
                "yAxes": [{"display": False}], # Hidden Y Axis
                "xAxes": [{
                    "display": True,
                    "gridLines": {"display": False, "drawBorder": False},
                    "ticks": {
                        "fontColor": "#999999", # Lighter text
                        "fontFamily": "Roboto, sans-serif",
                        "fontSize": 10,
                        "padding": 5
                    }
                }]
            }
        }
    }

    # Tweaks for other types
    if chart_type == "horizontalBar":
        config["options"]["scales"]["xAxes"][0]["display"] = False
        config["options"]["scales"]["yAxes"] = [{"display": True, "gridLines": {"display": False}, "ticks": {"fontColor": "#3E2723"}}]
    
    try:
        response = requests.post(
            "https://quickchart.io/chart/create",
            json={
                "chart": config,
                "width": 600,  # Wider
                "height": 250, # Taller
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
