import pytest
from src.agents.analyst import generate_daily_report

def test_ai_fallback_on_missing_key(mocker):
    mocker.patch("src.agents.analyst.GEMINI_API_KEY", None)
    report = generate_daily_report([], [])
    assert report["market_summary"] == "Market data analyzed. Check details below."

def test_ai_success_response(mocker):
    # Mock response object
    mock_response = mocker.Mock()
    mock_response.text = '{"market_summary": "Mock Summary", "news_summary": "Mock News", "chart_config": {"show": true, "type": "bar"}}'
    
    # Mock client instance
    mock_client = mocker.Mock()
    mock_client.models.generate_content.return_value = mock_response
    
    # Patch Client constructor to return our mock instance
    mocker.patch("google.genai.Client", return_value=mock_client)
    mocker.patch("src.agents.analyst.GEMINI_API_KEY", "fake_key")

    report = generate_daily_report([], [])
    assert report["market_summary"] == "Mock Summary"

def test_ai_cascade_failure(mocker):
    # Mock Client instance
    mock_client = mocker.Mock()
    # Configura o método para falhar SEMPRE (simulando 503/500 em todos os modelos)
    mock_client.models.generate_content.side_effect = Exception("500 Internal Error")
    
    mocker.patch("google.genai.Client", return_value=mock_client)
    mocker.patch("src.agents.analyst.GEMINI_API_KEY", "fake_key")
    
    # O código deve capturar a exceção e retornar o fallback, não explodir
    report = generate_daily_report([], [])
    
    assert report["market_summary"] == "Market data analyzed. Check details below."
