"""Carga del catálogo ficticio de productos (data/catalogo.json)."""

import json
from pathlib import Path

CATALOG_PATH = Path(__file__).parent / "data" / "catalogo.json"


def load_catalog() -> list[dict]:
    with open(CATALOG_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_catalog_json() -> str:
    """Versión en texto, para mandarle el catálogo a Gemini dentro del prompt."""
    return json.dumps(load_catalog(), ensure_ascii=False)
