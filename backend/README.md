# RecordShop AI — Backend

API en Python con [FastAPI](https://fastapi.tiangolo.com/).

## Requisitos

- Python 3.11+

## Cómo correrlo localmente

```bash
cd backend
py -m venv .venv
.venv\Scripts\Activate.ps1    # Windows (PowerShell)
# source .venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

La API queda en http://localhost:8001. Docs interactivas en http://localhost:8001/docs.

> Se usa el puerto **8001** en vez del clásico 8000 porque en Windows el 8000
> suele estar reservado por Hyper-V/WSL (`uvicorn` falla con `WinError 10013`).
> Si en tu máquina el 8000 anda, podés usar ese y ajustar `VITE_API_URL` en el frontend.

## Endpoints

| Método | Ruta       | Body                    | Respuesta                 | Para qué sirve                                  |
|--------|------------|-------------------------|----------------------------|-------------------------------------------------|
| GET    | `/health`  | —                       | `{"status": "ok"}`         | Health-check: probar que el server vive          |
| GET    | `/catalog` | —                       | lista de productos (JSON)  | Catálogo para mostrar en la página (no pasa por Gemini) |
| POST   | `/chat`    | `{"message": "..."}`    | `{"reply": "..."}`         | Le pasa el mensaje a Gemini junto con el catálogo y el system prompt |

`/chat` no guarda historial entre requests (fuera de alcance del proyecto,
ver `CLAUDE.md`). Si falta `GEMINI_API_KEY` devuelve 500 con un mensaje claro;
si Gemini falla (rate limit, red, etc.) devuelve 502.

**Rate limit propio:** además del límite de Gemini, `/chat` limita a 10
requests/minuto por IP (`rate_limit.py`) — sin esto, una sola visita
consultando rápido agota el límite de Gemini (compartido por todos) y rompe
el chat para cualquier otra persona navegando en simultáneo. Devuelve 429
si se supera.

Probarlo:

```bash
curl -X POST http://localhost:8001/chat -H "Content-Type: application/json" -d "{\"message\":\"tienen Kind of Blue?\"}"
```

## Tests

```bash
pip install -r requirements-dev.txt   # una vez, además de requirements.txt
pytest
```

No pegan a la API real de Gemini: `gemini_client` y `rate_limit` se prueban
mockeando el cliente (`unittest.mock`), y los tests de los endpoints
(`test_main.py`) mockean `ask_gemini` con FastAPI's `TestClient`. Corren en
menos de un segundo y no gastan cuota ni necesitan `GEMINI_API_KEY`.

## Variables de entorno

Copiar `../.env.example` a `backend/.env` y completar:

- `GEMINI_API_KEY` (obligatoria) — se consigue gratis en https://aistudio.google.com/apikey
- `GEMINI_MODEL` (opcional) — por default usa `gemini-flash-latest`
- `ALLOWED_ORIGIN` (opcional, solo producción) — URL del frontend deployado,
  para que CORS lo deje llamar a esta API. No hace falta en local.

## Estructura

```
backend/
├── main.py              # app FastAPI + endpoints (/health, /catalog, /chat)
├── gemini_client.py      # arma el prompt (system prompt + catálogo) y llama a Gemini
├── catalog.py            # carga data/catalogo.json (lo usan main.py y gemini_client.py)
├── rate_limit.py         # límite de requests/minuto por IP para /chat
├── requirements.txt
├── requirements-dev.txt  # + pytest, solo para desarrollo
├── pytest.ini
├── tests/
│   ├── conftest.py       # resetea el estado global entre tests
│   ├── test_catalog.py
│   ├── test_gemini_client.py
│   ├── test_rate_limit.py
│   └── test_main.py      # tests de los endpoints con TestClient
├── prompts/
│   └── system_prompt.py # instrucciones del chatbot para Gemini
└── data/
    └── catalogo.json    # catálogo ficticio de productos (datos de ejemplo)
```
