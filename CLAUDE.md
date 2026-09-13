# RecordShop AI — Contexto del proyecto

## Qué es este proyecto

Chatbot de soporte con IA para una tienda ficticia de CDs y vinilos. Es el **Proyecto 1** de un plan de aprendizaje de 16 meses hacia el rol de **Applied AI Engineer** (integración de LLMs en producto, no investigación/entrenamiento de modelos).

Es un proyecto de portfolio — el código debe quedar prolijo y bien documentado, pensado para mostrarlo a reclutadores.

## Stack técnico

- **Backend:** Python + FastAPI
- **Frontend:** React
- **LLM:** Google Gemini API (nivel gratuito, modelo Flash)
- **Control de versiones:** Git + GitHub (repo: `recordshop-ai`)

## Alcance funcional

El chatbot responde preguntas sobre:
- Política de envíos
- Política de devoluciones
- Catálogo de productos (CDs y vinilos ficticios — nombre, precio, stock, género)

**Fuera de alcance (a propósito, para no sobrecargar el proyecto):**
- Sin procesamiento de pagos real
- Sin login/autenticación de usuarios
- Sin memoria de conversación entre sesiones distintas (por ahora)

## Convenciones del proyecto

- **Commits:** en inglés, siguiendo Conventional Commits (`feat:`, `fix:`, `docs:`, etc.)
- **Documentación:** README completo con: qué es, stack, cómo correrlo localmente, decisiones técnicas
- **Seguridad:** la API key de Gemini SIEMPRE va en `.env` (nunca hardcodeada, nunca commiteada) — ya existe `.env.example` como plantilla
- **Estilo de código:** priorizar claridad sobre "código elegante" — es un proyecto de aprendizaje, cada decisión técnica debe poder explicarse en una entrevista

## Estructura de carpetas

```
recordshop-ai/
├── README.md
├── .gitignore
├── .env.example
├── scripts/                  # start-dev.ps1 / stop-dev.ps1 (levantar todo local)
├── backend/
│   ├── main.py                # endpoints: /health, /catalog, /chat
│   ├── gemini_client.py       # arma el prompt y llama a Gemini (con reintentos)
│   ├── catalog.py             # carga data/catalogo.json
│   ├── rate_limit.py          # límite de requests/minuto por IP en /chat
│   ├── requirements.txt
│   ├── requirements-dev.txt   # + pytest
│   ├── pytest.ini
│   ├── tests/                 # pytest, todo mockeado (no gasta cuota de Gemini)
│   ├── scripts/
│   │   └── fetch_covers.py    # busca portadas reales (iTunes Search API)
│   ├── prompts/
│   │   └── system_prompt.py
│   └── data/
│       └── catalogo.json      # catálogo ficticio, en inglés
└── frontend/
    ├── package.json
    └── src/
        ├── App.jsx             # layout: header, catálogo, chat, footer
        ├── Header.jsx          # menú + logo
        ├── Footer.jsx          # políticas + disclaimer
        ├── ProductGrid.jsx     # grilla de productos (consume /catalog)
        └── Chat.jsx            # interfaz de chat (consume /chat)
```

## Sobre quién trabaja en esto

Full-stack developer con 2 años de experiencia, cursando Licenciatura en Ciencia de Datos. Nivel de Python/SQL/ML: sólido en fundamentos (groupby, joins, window functions, train/test split, overfitting), reforzando indexación pandas (loc/iloc). Primera vez integrando una API de LLM — explicar conceptos de IA/LLMs con ejemplos simples cuando aparezcan por primera vez, sin asumir jerga previa no explicada.

## Estado actual del proyecto

- [x] Alcance definido
- [x] Stack elegido
- [x] Repo de GitHub creado
- [x] Estructura de carpetas inicial
- [x] Backend: endpoint básico de FastAPI (`GET /health`)
- [x] Backend: integración con Gemini API — `POST /chat` en `main.py`, arma el prompt en `gemini_client.py` (SDK `google-genai`, modelo `gemini-flash-latest`)
- [x] Catálogo ficticio de productos (JSON) — `data/catalogo.json` con 8 items, en inglés (mismo idioma que `prompts/system_prompt.py`); se pasa completo en cada request a `/chat`
- [x] Frontend: interfaz de chat básica — `Chat.jsx`, mensajes, input, loading y manejo de error
- [x] Conectar frontend con backend — ping a `/health` para mostrar el estado de conexión y `Chat.jsx` habla con `POST /chat`
- [x] Frontend: página tipo tienda — `Header.jsx` (menú), `ProductGrid.jsx` (catálogo con portadas reales, filtro por género, indicador de stock bajo), `Footer.jsx` (políticas); layout de dos columnas con el chat fijo a la derecha
- [x] Portadas reales del catálogo — `backend/scripts/fetch_covers.py` las busca en la iTunes Search API y las guarda en `data/catalogo.json`
- [x] Rate limit propio en `/chat` — `rate_limit.py`, 10 requests/minuto por IP, para no agotar el límite de Gemini (compartido por todos los visitantes)
- [x] Tests automatizados — `backend/tests/` con `pytest`, 21 tests mockeados (no gastan cuota de Gemini)
- [x] README completo — qué es, stack, cómo correrlo, decisiones técnicas (raíz + uno por carpeta)
- [ ] Deploy (a definir: Vercel para front, Render para back)

### Cómo correrlo localmente

Detalle completo en `README.md`. Resumen: dos terminales (o `.\scripts\start-dev.ps1`
desde la raíz para levantar las dos de una).

- **Backend:** `cd backend` → activar venv → `uvicorn main:app --reload --port 8001`
  → API en http://localhost:8001 (docs en `/docs`)
- **Frontend:** `cd frontend` → `npm run dev` → http://localhost:5173
- **Tests del backend:** `cd backend` → `pytest` (no necesita `GEMINI_API_KEY`, todo mockeado)

> **Puerto 8001, no 8000:** en el Windows de la dev el 8000 está reservado por
> Hyper-V/WSL y `uvicorn` falla con `WinError 10013`. El repo usa 8001 como
> default (`.env.example`, fallback en `App.jsx`, READMEs). CORS acepta cualquier
> puerto de `localhost` para tolerar que Vite salte de puerto.