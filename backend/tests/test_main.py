from unittest.mock import patch

from fastapi.testclient import TestClient

import rate_limit
from gemini_client import GeminiConfigError
from main import app

client = TestClient(app)


def test_health():
    res = client.get("/health")

    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_catalog_returns_the_product_list():
    res = client.get("/catalog")

    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "name" in data[0]


def test_chat_rejects_an_empty_message():
    res = client.post("/chat", json={"message": ""})

    assert res.status_code == 422


def test_chat_rejects_a_message_over_the_length_limit():
    res = client.post("/chat", json={"message": "a" * 2001})

    assert res.status_code == 422


def test_chat_returns_the_reply_on_success():
    with patch("main.ask_gemini", return_value="Mocked reply"):
        res = client.post("/chat", json={"message": "hi"})

    assert res.status_code == 200
    assert res.json() == {"reply": "Mocked reply"}


def test_chat_returns_500_when_gemini_is_not_configured():
    with patch("main.ask_gemini", side_effect=GeminiConfigError("Missing GEMINI_API_KEY")):
        res = client.post("/chat", json={"message": "hi"})

    assert res.status_code == 500
    assert "GEMINI_API_KEY" in res.json()["detail"]


def test_chat_returns_502_when_gemini_call_fails():
    with patch("main.ask_gemini", side_effect=RuntimeError("Gemini blew up")):
        res = client.post("/chat", json={"message": "hi"})

    assert res.status_code == 502
    assert res.json()["detail"] == "Gemini blew up"


def test_chat_gets_rate_limited_after_too_many_requests():
    with patch("main.ask_gemini", return_value="ok"):
        for _ in range(rate_limit.MAX_REQUESTS):
            res = client.post("/chat", json={"message": "hi"})
            assert res.status_code == 200

        res = client.post("/chat", json={"message": "hi"})

    assert res.status_code == 429
