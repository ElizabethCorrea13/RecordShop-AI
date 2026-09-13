import pytest

import gemini_client
import rate_limit


@pytest.fixture(autouse=True)
def _reset_module_state():
    """gemini_client y rate_limit guardan estado global (cliente de Gemini
    cacheado, contador de requests por IP). Sin resetear esto antes y
    después de cada test, uno podía dejar contaminado el siguiente.
    """
    gemini_client._client = None
    rate_limit._requests_by_ip.clear()
    yield
    gemini_client._client = None
    rate_limit._requests_by_ip.clear()
