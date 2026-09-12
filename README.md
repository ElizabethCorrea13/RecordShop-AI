# RecordShop-AI

Chatbot de soporte con IA para una tienda ficticia de CDs y vinilos.
Proyecto de portfolio — **FastAPI + React + Gemini API**.

Responde preguntas sobre política de envíos, política de devoluciones y el
catálogo de productos. Sin pagos reales, sin login, sin memoria entre sesiones
(fuera de alcance a propósito).

## Stack

- **Backend:** Python + FastAPI
- **Frontend:** React + Vite
- **LLM:** Google Gemini API (nivel gratuito, modelo Flash) — *pendiente de integrar*

## Estructura

```
recordshop-ai/
├── .env.example          # plantilla de variables de entorno del backend
├── backend/              # API FastAPI
│   ├── main.py           # app + endpoint /health
│   ├── requirements.txt
│   └── data/
│       └── catalogo.json # catálogo ficticio (datos de ejemplo)
└── frontend/             # interfaz de chat (React + Vite)
    ├── index.html
    ├── package.json
    └── src/
```

## Cómo correrlo localmente

Hacen falta **dos terminales**: una para el backend y otra para el frontend.

### 1. Backend

```bash
cd backend
py -m venv .venv
.venv\Scripts\Activate.ps1    # Windows (PowerShell)
# source .venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

API en http://localhost:8001 · docs en http://localhost:8001/docs

> Puerto **8001**: en Windows el 8000 suele estar reservado por Hyper-V/WSL y
> `uvicorn` falla con `WinError 10013`. Si en tu máquina el 8000 anda, usalo y
> ajustá `VITE_API_URL` en `frontend/.env`.
>
> Si PowerShell bloquea `Activate.ps1`, corré una vez:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

Probar el health-check:

```bash
curl http://localhost:8001/health
# {"status":"ok"}
```

### 2. Frontend

```bash
cd frontend
npm install
cp .env.example .env          # PowerShell: Copy-Item .env.example .env
npm run dev
```

App en http://localhost:5173. Muestra un indicador de si el backend responde.

### Atajo: levantar todo con un script

Una vez instaladas las dependencias de ambos lados (pasos 1 y 2 de arriba, aunque
sea una vez), se puede levantar todo con un solo comando desde la raíz:

```powershell
.\scripts\start-dev.ps1
```

Abre backend y frontend cada uno en su propia ventana de PowerShell. Para
frenar los dos de una:

```powershell
.\scripts\stop-dev.ps1
```

`stop-dev.ps1` no se limita a mirar qué proceso "dice" Windows que tiene
ocupado el puerto (`uvicorn --reload` deja procesos hijos que Windows a veces
reporta mal): mata el árbol completo de procesos de cada ventana, así no
quedan servidores huérfanos corriendo en segundo plano.

## Estado actual

Esqueleto funcionando: endpoint `/health` en el backend y app de React que lo
consume. Todavía falta la integración con Gemini y la interfaz de chat.

## Decisiones técnicas

- **Vite en lugar de Create React App** — CRA está discontinuado; Vite es el
  scaffold recomendado hoy para SPAs de React (arranque y HMR más rápidos).
- **CORS habilitado sólo para `localhost:5173`** — el navegador bloquea las
  llamadas entre orígenes distintos; se abre explícitamente el del frontend de
  desarrollo.
- **La API key de Gemini vive en `backend/.env`** — nunca hardcodeada ni
  commiteada; `.env.example` queda como plantilla.

### Políticas de la tienda (ficticias, para este proyecto)

**Envíos:**
- Estándar: 5-7 días hábiles, $1500
- Express: 2-3 días hábiles, $3500
- Gratis en compras +$15000
- Cobertura: todo el país

**Devoluciones:**
- 30 días desde la recepción
- Producto sin usar, en empaque original
- Vinilos: sello de calidad no debe estar roto
- Reembolso en 5-10 días hábiles
- Productos en oferta/liquidación: sin devolución, solo cambio

### Por qué el catálogo se pasa completo en cada consulta

Con 8 productos es simple pasarle todo el catálogo al modelo en cada llamada. No escala a catálogos grandes — esa limitación se resuelve en el Proyecto 2 con RAG (retrieval en vez de mandar todo siempre).