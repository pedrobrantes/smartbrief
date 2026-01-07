import pytest
from src.collectors.trends import get_google_trends

def test_trends_google_block_fallback(mocker):
    # Mock requests.get to return 429 Too Many Requests
    mock_response = mocker.Mock()
    mock_response.status_code = 429
    
    mocker.patch("requests.get", return_value=mock_response)
    
    # Run collector
    trends = get_google_trends()
    
    # Assert we got fallback items (User Keywords) instead of crash
    assert len(trends) > 0
    assert trends[0]["traffic"] == "Interest"
    # Check if the first trend matches one of your keywords
    from src.settings import KEYWORDS
    assert trends[0]["title"] == KEYWORDS[0]
