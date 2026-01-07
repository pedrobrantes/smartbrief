from src.visualizers.charts import generate_sparkline_url

def test_generate_sparkline_valid(mocker):
    # Mock requests.post
    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"url": "https://quickchart.io/chart/render/fake-uuid"}

    data = [10.0, 12.0, 11.5, 13.0]
    url = generate_sparkline_url(data, is_positive=True)
    
    # 1. Verifica se retornou a URL do mock
    assert url == "https://quickchart.io/chart/render/fake-uuid"
    
    # 2. Verifica se o payload enviado continha a cor VERDE (Gain)
    # Acessamos os argumentos que foram passados para requests.post
    args, kwargs = mock_post.call_args
    sent_json = str(kwargs['json']) # Converte o dict para string para facilitar a busca
    assert "2E7D32" in sent_json 

def test_generate_sparkline_loss(mocker):
    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"url": "https://quickchart.io/chart/render/fake-uuid"}

    data = [10.0, 9.0, 8.0]
    generate_sparkline_url(data, is_positive=False)
    
    # Verifica se o payload enviado continha a cor VERMELHA (Loss)
    args, kwargs = mock_post.call_args
    sent_json = str(kwargs['json'])
    assert "C62828" in sent_json

def test_generate_sparkline_empty():
    url = generate_sparkline_url([], True)
    assert url is None
