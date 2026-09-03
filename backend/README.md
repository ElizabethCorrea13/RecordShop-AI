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

| Método | Ruta      | Respuesta            | Para qué sirve                          |
|--------|-----------|----------------------|----------------------------------------|
| GET    | `/health` | `{"status": "ok"}`   | Health-check: probar que el server vive  |

## Variables de entorno

Copiar `../.env.example` a `backend/.env` y completar. Por ahora sólo hará falta
`GEMINI_API_KEY` cuando se integre el LLM (todavía no se usa).

## Estructura

```
backend/
├── main.py              # app FastAPI + endpoints
├── requirements.txt
└── data/
    └── catalogo.json    # catálogo ficticio de productos (datos de ejemplo)
```
