import pytest
from unittest.mock import patch, Mock
from src.adapters.providers.amadeus_adapter import AmadeusAdapter
from src.domain.exceptions import AdapterError


class TestAmadeusAdapter:

    @patch("src.adapters.providers.amadeus_adapter.requests.post")
    @patch("src.adapters.providers.amadeus_adapter.requests.get")
    def test_returns_raw_json_on_success(self, mock_get, mock_post, mock_amadeus_response):
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: {"access_token": "test_token", "expires_in": 1799}
        )
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: mock_amadeus_response
        )
        adapter = AmadeusAdapter(api_key="test_key", api_secret="test_secret")
        result = adapter.search_flights(
            origin="YUL",
            destination="LAX",
            departure_date="2026-04-15",
        )
        assert "data" in result

    @patch("src.adapters.providers.amadeus_adapter.requests.post")
    @patch("src.adapters.providers.amadeus_adapter.requests.get")
    def test_response_contains_data_key(self, mock_get, mock_post, mock_amadeus_response):
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: {"access_token": "test_token", "expires_in": 1799}
        )
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: mock_amadeus_response
        )
        adapter = AmadeusAdapter(api_key="test_key", api_secret="test_secret")
        result = adapter.search_flights(
            origin="YUL",
            destination="LAX",
            departure_date="2026-04-15",
        )
        assert isinstance(result["data"], list)

    @patch("src.adapters.providers.amadeus_adapter.requests.post")
    @patch("src.adapters.providers.amadeus_adapter.requests.get")
    def test_raises_adapter_error_on_http_error(self, mock_get, mock_post):
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: {"access_token": "test_token", "expires_in": 1799}
        )
        mock_get.return_value = Mock(status_code=500)
        adapter = AmadeusAdapter(api_key="test_key", api_secret="test_secret")
        with pytest.raises(AdapterError):
            adapter.search_flights(
                origin="YUL",
                destination="LAX",
                departure_date="2026-04-15",
            )

    @patch("src.adapters.providers.amadeus_adapter.requests.post")
    @patch("src.adapters.providers.amadeus_adapter.requests.get")
    def test_raises_adapter_error_on_timeout(self, mock_get, mock_post):
        import requests
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: {"access_token": "test_token", "expires_in": 1799}
        )
        mock_get.side_effect = requests.exceptions.Timeout()
        adapter = AmadeusAdapter(api_key="test_key", api_secret="test_secret")
        with pytest.raises(AdapterError):
            adapter.search_flights(
                origin="YUL",
                destination="LAX",
                departure_date="2026-04-15",
            )
