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

# El tier gratis de Gemini devuelve 503 (modelo saturado) con bastante
# frecuencia, y casi siempre se resuelve solo unos segundos después: vale la
# pena reintentar un par de veces antes de darnos por vencidos.
#
# 429 es otra historia: es el límite de requests por minuto del tier gratis
# (20/min), y Google pide esperar del orden de 30-60s, no unos segundos —
# reintentar rápido como con el 503 no sirve de nada, así que para el 429 no
# reintentamos y directamente avisamos que es un límite de uso, no una caída.
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
            if e.code == 429:
                break  # no sirve reintentar rápido, ver comentario arriba
            if not isinstance(e, ServerError) or attempt == MAX_RETRIES:
                break
            logger.warning(
                "Gemini call failed (%s), retrying %d/%d: %s",
                e.code, attempt + 1, MAX_RETRIES, e,
            )
            time.sleep(RETRY_DELAY_SECONDS * (attempt + 1))

    logger.error("Gemini call failed: %s", last_error)

    if last_error is not None and last_error.code == 429:
        raise RuntimeError(
            "The assistant has hit Gemini's free-tier rate limit (requests "
            "per minute). Please wait about a minute and try again."
        ) from last_error

    raise RuntimeError(
        "The assistant is temporarily unavailable — Gemini's free tier is "
        "under heavy demand right now. Please try again in a moment."
    ) from last_error
