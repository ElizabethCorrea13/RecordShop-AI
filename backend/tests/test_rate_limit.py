import time
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

import rate_limit


def _fake_request(ip="1.2.3.4", forwarded=None):
    request = MagicMock()
    request.headers = {"x-forwarded-for": forwarded} if forwarded else {}
    request.client = MagicMock(host=ip)
    return request


def test_allows_requests_under_the_limit():
    request = _fake_request()
    for _ in range(rate_limit.MAX_REQUESTS):
        rate_limit.enforce_chat_rate_limit(request)  # no debería tirar nada


def test_blocks_the_request_that_goes_over_the_limit():
    request = _fake_request()
    for _ in range(rate_limit.MAX_REQUESTS):
        rate_limit.enforce_chat_rate_limit(request)

    with pytest.raises(HTTPException) as exc_info:
        rate_limit.enforce_chat_rate_limit(request)

    assert exc_info.value.status_code == 429


def test_limit_is_tracked_per_ip():
    busy_ip = _fake_request(ip="1.1.1.1")
    other_ip = _fake_request(ip="2.2.2.2")

    for _ in range(rate_limit.MAX_REQUESTS):
        rate_limit.enforce_chat_rate_limit(busy_ip)

    # busy_ip ya llegó al límite, pero other_ip es una IP distinta
    rate_limit.enforce_chat_rate_limit(other_ip)


def test_uses_x_forwarded_for_when_present():
    request = _fake_request(ip="proxy-ip", forwarded="real-client-ip, proxy-ip")
    assert rate_limit._client_ip(request) == "real-client-ip"


def test_falls_back_to_request_client_host_without_proxy_header():
    request = _fake_request(ip="1.2.3.4")
    assert rate_limit._client_ip(request) == "1.2.3.4"


def test_old_requests_fall_out_of_the_window(monkeypatch):
    request = _fake_request()
    current_time = [1_000.0]
    monkeypatch.setattr(time, "monotonic", lambda: current_time[0])

    for _ in range(rate_limit.MAX_REQUESTS):
        rate_limit.enforce_chat_rate_limit(request)

    # avanzamos el reloj más allá de la ventana: el contador se resetea solo
    current_time[0] += rate_limit.WINDOW_SECONDS + 1
    rate_limit.enforce_chat_rate_limit(request)  # no debería tirar nada
