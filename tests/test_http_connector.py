import pytest
from unittest.mock import patch, MagicMock
from core.http_connector import HttpConnector


def _mock_response(json_data, status_code=200):
    mock = MagicMock()
    mock.status_code = status_code
    mock.json.return_value = json_data
    mock.raise_for_status = MagicMock()
    return mock


def test_get_returns_json():
    connector = HttpConnector("http://api:8003")
    with patch("requests.get", return_value=_mock_response({"key": "val"})) as mock_get:
        result = connector.get("/bikes")
        assert result == {"key": "val"}
        mock_get.assert_called_once_with("http://api:8003/bikes")


def test_get_strips_trailing_slash_from_base():
    connector = HttpConnector("http://api:8003/")
    with patch("requests.get", return_value=_mock_response([])) as mock_get:
        connector.get("/path")
        mock_get.assert_called_once_with("http://api:8003/path")


def test_get_raises_on_http_error():
    connector = HttpConnector("http://api:8003")
    mock_resp = _mock_response({}, status_code=500)
    mock_resp.raise_for_status.side_effect = Exception("500 Server Error")
    with patch("requests.get", return_value=mock_resp):
        with pytest.raises(Exception, match="500 Server Error"):
            connector.get("/bikes")
