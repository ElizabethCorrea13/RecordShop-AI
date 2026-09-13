"""
Busca la portada de cada álbum del catálogo en la iTunes Search API
(pública, sin API key) y la guarda como campo "cover" en data/catalogo.json.

Es un script de un solo uso para completar los datos del catálogo, no
corre en el server. Volver a correrlo pisa las portadas existentes.

Uso (desde backend/, con el venv activado):
    python scripts/fetch_covers.py
"""

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

CATALOG_PATH = Path(__file__).parent.parent / "data" / "catalogo.json"
ARTWORK_SIZE = "600x600bb"  # iTunes sirve el mismo archivo en otros tamaños cambiando esto en la URL


def fetch_cover(artist: str, name: str) -> str | None:
    query = urllib.parse.quote(f"{artist} {name}")
    url = f"https://itunes.apple.com/search?term={query}&entity=album&limit=10"
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.load(resp)

    results = data.get("results") or []
    if not results:
        return None

    # No asumir que el primer resultado es el correcto: para búsquedas
    # ambiguas iTunes a veces devuelve primero otro álbum del mismo artista
    # (ej. "Taylor Swift evermore" trajo "folklore" como resultado #1).
    # Preferir un match exacto de título; si no hay, recién ahí usar el primero.
    exact = [r for r in results if r.get("collectionName", "").strip().lower() == name.lower()]
    best = exact[0] if exact else results[0]

    artwork = best.get("artworkUrl100")
    if not artwork:
        return None
    return artwork.replace("100x100bb", ARTWORK_SIZE)


def main():
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

    for item in catalog:
        cover = fetch_cover(item["artist"], item["name"])
        if cover:
            item["cover"] = cover
            print(f"OK   {item['artist']} - {item['name']}")
        else:
            print(f"???  {item['artist']} - {item['name']} (sin resultado en iTunes)")
        time.sleep(0.3)  # prudente con una API pública sin key

    CATALOG_PATH.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
