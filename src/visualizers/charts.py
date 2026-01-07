import requests
from src.settings import CHART_THEME

def generate_sparkline_url(data_points, is_positive):
    # ... (código do sparkline permanece igual) ...
    if not data_points: return None
    
    color = f"#{CHART_THEME['gain']}" if is_positive else f"#{CHART_THEME['loss']}"
    
    config = {
        "type": "line",
        "data": {
            "labels": list(range(len(data_points))),
            "datasets": [{
                "data": data_points,
                "borderColor": color,
                "borderWidth": 4,
                "fill": False,
                "pointRadius": 0,
                "tension": 0.4
            }]
        },
        "options": {
            "legend": {"display": False},
            "scales": {
                "xAxes": [{"display": False}],
                "yAxes": [{"display": False}]
            },
            "layout": {"padding": 5}
        }
    }

    try:
        response = requests.post(
            "https://quickchart.io/chart/create",
            json={
                "chart": config,
                "width": 120,
                "height": 50,
                "backgroundColor": "transparent",
                "format": "png",
                "version": "2"
            },
            timeout=5
        )
        if response.status_code == 200:
            return response.json().get('url')
    except:
        return None

def generate_chart_url(data, chart_type="bar"):
    if not data or chart_type == "none":
        return None

    labels = [d['name'] for d in data]
    values = [d['change'] for d in data]
    # Adicionando # para garantir que o QuickChart entenda como Hex
    colors = [f"#{CHART_THEME['gain']}" if v >= 0 else f"#{CHART_THEME['loss']}" for v in values]

    config = {
        "type": chart_type,
        "data": {
            "labels": labels,
            "datasets": [{
                "data": values,
                "backgroundColor": colors,
                # Reduzi o borderRadius para evitar bugs visuais em barras pequenas
                "borderRadius": 4, 
                "borderSkipped": False,
            }]
        },
        "options": {
            "devicePixelRatio": 2.0,
            "legend": {"display": False},
            "layout": {"padding": {"top": 10, "bottom": 10, "left": 10, "right": 10}},
            "scales": {
                # Garante que o eixo Y (valores) apareça, mas sem linhas de grade feias
                "yAxes": [{"display": False}],
                "xAxes": [{
                    "display": True,
                    "gridLines": {"display": False, "drawBorder": False},
                    "ticks": {
                        "fontColor": "#999999",
                        "fontFamily": "Roboto, sans-serif",
                        "fontSize": 10,
                        "padding": 5
                    }
                }]
            }
        }
    }

    # Ajuste para gráfico horizontal
    if chart_type == "horizontalBar":
        config["options"]["scales"]["xAxes"][0]["display"] = False
        # No horizontal, mostramos os nomes no eixo Y
        config["options"]["scales"]["yAxes"] = [{
            "display": True, 
            "gridLines": {"display": False}, 
            "ticks": {"fontColor": "#3E2723", "fontSize": 10}
        }]
    
    try:
        response = requests.post(
            "https://quickchart.io/chart/create",
            json={
                "chart": config,
                "width": 600,
                "height": 300, # Aumentei altura para dar espaço
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
