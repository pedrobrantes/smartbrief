import requests
from src.settings import CHART_THEME

def generate_chart_url(data):
    if not data:
        return None

    labels = [d['name'] for d in data]
    values = [d['change'] for d in data]
    colors = [CHART_THEME['gain'] if v >= 0 else CHART_THEME['loss'] for v in values]

    config = {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": [{
                "data": values,
                "backgroundColor": colors,
                "borderRadius": 50,
                "borderSkipped": False,
                "barThickness": 20
            }]
        },
        "options": {
            "legend": {"display": False},
            "scales": {
                "yAxes": [{"display": False}],
                "xAxes": [{
                    "gridLines": {"display": False},
                    "ticks": {
                        "fontColor": CHART_THEME['text'],
                        "fontFamily": "sans-serif",
                        "fontSize": 10
                    }
                }]
            }
        }
    }

    try:
        response = requests.post(
            "
