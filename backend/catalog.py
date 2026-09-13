"""Carga del catálogo ficticio de productos (data/catalogo.json)."""

import json
from pathlib import Path

CATALOG_PATH = Path(__file__).parent / "data" / "catalogo.json"


def load_catalog() -> list[dict]:
    with open(CATALOG_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_catalog_json() -> str:
    """Versión en texto para el prompt de Gemini.

    Saca el campo "cover" (URL de la portada): es para la página, a
    Gemini no le sirve para responder y solo suma tokens de más.
    """
    catalog_without_covers = [
        {k: v for k, v in item.items() if k != "cover"} for item in load_catalog()
    ]
    return json.dumps(catalog_without_covers, ensure_ascii=False)
