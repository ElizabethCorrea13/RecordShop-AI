"""
Cliente de Gemini para el chatbot de soporte.

Arma el prompt (system prompt + catálogo completo + mensaje del cliente) y
llama a la API de Gemini. Sin memoria entre requests: cada llamada es
independiente, no se guarda historial de conversación (fuera de alcance
del proyecto, ver CLAUDE.md).
"""

import logging
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError, ServerError

from catalog import load_catalog_json
from prompts.system_prompt import SYSTEM_PROMPT

load_dotenv()
logger = logging.getLogger(__name__)

# "gemini-flash-latest" es un alias que siempre apunta al modelo Flash vigente,
# así no hay que actualizar el código cada vez que Google saca una versión
# nueva. Se puede fijar una versión puntual con la variable GEMINI_MODEL.
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

# El tier gratis de Gemini devuelve 503 (modelo saturado) o 429 (rate limit)
# con bastante frecuencia, y casi siempre son errores transitorios que se
# resuelven solos unos segundos después. En vez de mostrarle eso al usuario
# a la primera, reintentamos un par de veces antes de darnos por vencidos.
MAX_RETRIES = 2
RETRY_DELAY_SECONDS = 1.5

_client: genai.Client | None = None


class GeminiConfigError(RuntimeError):
    """La API key de Gemini no está configurada."""


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise GeminiConfigError(
                "Missing GEMINI_API_KEY. Copy .env.example to backend/.env and "
                "fill in the key (https://aistudio.google.com/apikey)."
            )
        _client = genai.Client(api_key=api_key)
    return _client


def _is_transient(error: APIError) -> bool:
    """503 (saturado) y 5xx en general son de Google; 429 es rate limit."""
    return isinstance(error, ServerError) or error.code == 429


def ask(message: str) -> str:
    """Envía un mensaje del cliente a Gemini con el system prompt y el catálogo."""
    client = _get_client()
    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"PRODUCT CATALOG (JSON):\n{load_catalog_json()}\n\n"
        f"CUSTOMER MESSAGE:\n{message}"
    )

    last_error: APIError | None = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
            if not response.text:
                raise RuntimeError("Gemini didn't return any text in the response.")
            return response.text
        except APIError as e:
            last_error = e
            if not _is_transient(e) or attempt == MAX_RETRIES:
                break
            logger.warning(
                "Gemini call failed (%s), retrying %d/%d: %s",
                e.code, attempt + 1, MAX_RETRIES, e,
            )
            time.sleep(RETRY_DELAY_SECONDS * (attempt + 1))

    logger.error("Gemini call failed after retries: %s", last_error)
    raise RuntimeError(
        "The assistant is temporarily unavailable — Gemini's free tier is "
        "under heavy demand right now. Please try again in a moment."
    ) from last_error
