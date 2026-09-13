"""
RecordShop AI — API backend.

Expone el health-check, el catálogo de productos y el endpoint de chat,
que arma un prompt con el catálogo completo y llama a Gemini (ver
gemini_client.py).

Cómo correrlo (desde la carpeta backend/, con el venv activado):
    uvicorn main:app --reload --port 8001
"""

import os

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from catalog import load_catalog
from gemini_client import GeminiConfigError, ask as ask_gemini
from rate_limit import enforce_chat_rate_limit

app = FastAPI(title="RecordShop AI API", version="0.1.0")

# CORS = Cross-Origin Resource Sharing. El navegador bloquea por defecto que
# una página servida desde un origen (ej. http://localhost:5173, donde corre
# el frontend) haga fetch a otro origen (esta API). Este middleware le dice a
# FastAPI que agregue las cabeceras que autorizan al frontend a llamar a la API.
#
# En desarrollo se acepta cualquier puerto de localhost/127.0.0.1 vía regex,
# porque Vite salta de puerto si el anterior está ocupado (5173, 5174, ...).
# En producción el frontend vive en otro dominio (ej. Vercel), así que ese se
# agrega aparte, leído de la variable de entorno ALLOWED_ORIGIN — no viene
# hardcodeado porque no se conoce hasta que el frontend esté deployado.
ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN] if ALLOWED_ORIGIN else [],
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    """Health-check simple: sirve para monitoreo y para probar el deploy."""
    return {"status": "ok"}


@app.get("/catalog")
def catalog():
    """Catálogo de productos, para mostrarlo en la página (no pasa por Gemini)."""
    return load_catalog()


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    reply: str


@app.post(
    "/chat",
    response_model=ChatResponse,
    dependencies=[Depends(enforce_chat_rate_limit)],
)
def chat(payload: ChatRequest):
    """Recibe un mensaje del cliente y devuelve la respuesta de Gemini.

    Sin memoria entre requests: cada llamada es independiente (fuera de
    alcance del proyecto guardar historial entre sesiones). Limitado por IP
    (ver rate_limit.py) para que una sola visita no agote el límite de
    requests/minuto de Gemini, que es compartido por todos.
    """
    try:
        reply = ask_gemini(payload.message)
    except GeminiConfigError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e
    return ChatResponse(reply=reply)
