import httpx
import pytest
from unittest.mock import patch

from assistant_api.exchange import ExchangeClient, ExternalServiceError


def test_exchange_success_updates_cache():
    client = ExchangeClient()

    mock_request = httpx.Request("GET", "https://fake.url")
    mock_response = httpx.Response(200, json={"rates": {"VND": 25400}}, request=mock_request)

    with patch("httpx.Client.get", return_value=mock_response):
        result = client.current_rate()

        assert result["rate"] == 25400
        assert result["stale"] is False
        assert client._cache == result


def test_exchange_timeout_returns_stale_data():
    client = ExchangeClient()
    client._cache = {"currency": "USD to VND", "rate": 24000, "stale": False}

    with patch("httpx.Client.get", side_effect=httpx.ConnectTimeout("Timeout")):
        result = client.current_rate()

        assert result["rate"] == 24000
        assert result["stale"] is True


def test_exchange_upstream_500_triggers_retry_and_fallback():
    client = ExchangeClient()
    client._cache = {"currency": "USD to VND", "rate": 24000, "stale": False}

    # Đã có request giả ở đây
    mock_request = httpx.Request("GET", "https://fake.url")
    mock_response = httpx.Response(500, request=mock_request)

    with patch("httpx.Client.get", return_value=mock_response):
        result = client.current_rate()

        assert result["rate"] == 24000
        assert result["stale"] is True


def test_exchange_malformed_json_handled_gracefully():
    client = ExchangeClient()
    client._cache = {"currency": "USD to VND", "rate": 24000, "stale": False}

    mock_request = httpx.Request("GET", "https://fake.url")
    mock_response = httpx.Response(200, content=b"This is not JSON", request=mock_request)

    with patch("httpx.Client.get", return_value=mock_response):
        result = client.current_rate()

        assert result["rate"] == 24000
        assert result["stale"] is True


def test_exchange_no_cache_returns_503():
    client = ExchangeClient()
    client._cache = None

    with patch("httpx.Client.get", side_effect=httpx.ConnectTimeout("Timeout")):
        with pytest.raises(ExternalServiceError):
            client.current_rate()