"""
Rate limiting simple por IP para /chat.

Por qué: el límite de requests/minuto que Gemini le pone al tier gratis
(20/min, ver gemini_client.py) es compartido por TODOS los que usen la app,
no por usuario. Sin este control, una sola visita haciendo muchas preguntas
seguidas (o un bot) puede agotarlo y dejar el chat roto para cualquier otra
persona que esté navegando en simultáneo.

En memoria y por proceso: alcanza para un servidor como este. Si el día de
mañana esto corre en varias instancias, este contador dejaría de ser
compartido entre ellas y habría que centralizarlo (Redis, por ejemplo).
"""

import threading
import time
from collections import defaultdict

from fastapi import HTTPException, Request

MAX_REQUESTS = 10
WINDOW_SECONDS = 60

_lock = threading.Lock()
_requests_by_ip: dict[str, list[float]] = defaultdict(list)


def _client_ip(request: Request) -> str:
    # Detrás de un proxy (ej. Render en producción) la IP real del visitante
    # viene en X-Forwarded-For; request.client.host ahí sería la del proxy.
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def enforce_chat_rate_limit(request: Request) -> None:
    """Dependencia de FastAPI: corta con 429 si esta IP se pasó del límite."""
    ip = _client_ip(request)
    now = time.monotonic()

    with _lock:
        recent = [t for t in _requests_by_ip[ip] if now - t < WINDOW_SECONDS]
        if len(recent) >= MAX_REQUESTS:
            raise HTTPException(
                status_code=429,
                detail=(
                    f"You're sending messages too quickly (limit: "
                    f"{MAX_REQUESTS} per minute). Please wait a bit and try again."
                ),
            )
        recent.append(now)
        _requests_by_ip[ip] = recent
