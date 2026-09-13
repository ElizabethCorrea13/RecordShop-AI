"""
Cliente de Gemini para el chatbot de soporte.

Arma el prompt (system prompt + catálogo completo + mensaje del cliente) y
llama a la API de Gemini. Sin memoria entre requests: cada llamada es
independiente, no se guarda historial de conversación (fuera de alcance
del proyecto, ver CLAUDE.md).
"""

import os

from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

from catalog import load_catalog_json
from prompts.system_prompt import SYSTEM_PROMPT

load_dotenv()

# "gemini-flash-latest" es un alias que siempre apunta al modelo Flash vigente,
# así no hay que actualizar el código cada vez que Google saca una versión
# nueva. Se puede fijar una versión puntual con la variable GEMINI_MODEL.
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

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
    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    except APIError as e:
        raise RuntimeError(f"Error calling the Gemini API: {e}") from e

    if not response.text:
        raise RuntimeError("Gemini didn't return any text in the response.")
    return response.text
