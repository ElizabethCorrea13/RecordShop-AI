from unittest.mock import MagicMock, patch

import pytest
from google.genai.errors import ClientError, ServerError

import gemini_client


def _server_error(code=503, status="UNAVAILABLE"):
    return ServerError(code, {"error": {"code": code, "message": "busy", "status": status}})


def _rate_limit_error():
    return ClientError(429, {"error": {"code": 429, "message": "quota", "status": "RESOURCE_EXHAUSTED"}})


def test_ask_raises_config_error_without_api_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    with pytest.raises(gemini_client.GeminiConfigError):
        gemini_client.ask("hello")


def test_ask_retries_transient_server_error_then_succeeds(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    fake_response = MagicMock(text="ok after retry")
    calls = {"n": 0}

    def flaky(model, contents):
        calls["n"] += 1
        if calls["n"] < 2:
            raise _server_error()
        return fake_response

    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = flaky

    with patch("time.sleep"), patch.object(gemini_client, "_get_client", return_value=mock_client):
        result = gemini_client.ask("hello")

    assert result == "ok after retry"
    assert calls["n"] == 2


def test_ask_gives_up_after_max_retries(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    calls = {"n": 0}

    def always_fails(model, contents):
        calls["n"] += 1
        raise _server_error()

    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = always_fails

    with patch("time.sleep"), patch.object(gemini_client, "_get_client", return_value=mock_client):
        with pytest.raises(RuntimeError, match="temporarily unavailable"):
            gemini_client.ask("hello")

    assert calls["n"] == gemini_client.MAX_RETRIES + 1


def test_ask_does_not_retry_rate_limit_and_uses_specific_message(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    calls = {"n": 0}

    def rate_limited(model, contents):
        calls["n"] += 1
        raise _rate_limit_error()

    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = rate_limited

    with patch("time.sleep") as mock_sleep, patch.object(gemini_client, "_get_client", return_value=mock_client):
        with pytest.raises(RuntimeError, match="rate limit"):
            gemini_client.ask("hello")

    # el 429 no se reintenta rapido: una sola llamada, sin espera
    assert calls["n"] == 1
    mock_sleep.assert_not_called()


def test_ask_raises_when_gemini_returns_no_text(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake-key")
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = MagicMock(text="")

    with patch.object(gemini_client, "_get_client", return_value=mock_client):
        with pytest.raises(RuntimeError, match="didn't return any text"):
            gemini_client.ask("hello")
