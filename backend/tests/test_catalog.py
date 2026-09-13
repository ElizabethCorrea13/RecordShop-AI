import json

from catalog import load_catalog, load_catalog_json

REQUIRED_FIELDS = {"id", "name", "artist", "format", "genre", "price", "stock", "description"}


def test_load_catalog_returns_products_with_expected_fields():
    catalog = load_catalog()

    assert isinstance(catalog, list)
    assert len(catalog) > 0
    for item in catalog:
        assert REQUIRED_FIELDS <= item.keys()


def test_load_catalog_json_strips_cover_but_keeps_the_rest():
    catalog = load_catalog()
    assert any("cover" in item for item in catalog), "el catálogo real debería traer portadas"

    for_prompt = json.loads(load_catalog_json())

    assert len(for_prompt) == len(catalog)
    assert all("cover" not in item for item in for_prompt)
    # el resto de los campos no se toca, solo se saca "cover"
    assert for_prompt[0]["name"] == catalog[0]["name"]
    assert for_prompt[0]["price"] == catalog[0]["price"]
