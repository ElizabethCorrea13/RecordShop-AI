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
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── data/
│       └── catalogo.json
└── frontend/
    ├── src/
    └── package.json
```

## Sobre quién trabaja en esto

Full-stack developer con 2 años de experiencia, cursando Licenciatura en Ciencia de Datos. Nivel de Python/SQL/ML: sólido en fundamentos (groupby, joins, window functions, train/test split, overfitting), reforzando indexación pandas (loc/iloc). Primera vez integrando una API de LLM — explicar conceptos de IA/LLMs con ejemplos simples cuando aparezcan por primera vez, sin asumir jerga previa no explicada.

## Estado actual del proyecto

- [x] Alcance definido
- [x] Stack elegido
- [ ] Repo de GitHub creado
- [x] Estructura de carpetas inicial
- [x] Backend: endpoint básico de FastAPI (`GET /health`)
- [ ] Backend: integración con Gemini API
- [~] Catálogo ficticio de productos (JSON) — hay `data/catalogo.json` con 4 items de ejemplo; todavía no se sirve por la API
- [ ] Frontend: interfaz de chat básica
- [~] Conectar frontend con backend — el frontend ya hace ping a `/health` y muestra el estado de conexión; falta el chat
- [ ] README completo
- [ ] Deploy (a definir: Vercel para front, Render para back)

### Cómo correrlo localmente

Detalle completo en `README.md`. Resumen: dos terminales.

- **Backend:** `cd backend` → activar venv → `uvicorn main:app --reload --port 8001`
  → API en http://localhost:8001 (docs en `/docs`)
- **Frontend:** `cd frontend` → `npm run dev` → http://localhost:5173

> **Puerto 8001, no 8000:** en el Windows de la dev el 8000 está reservado por
> Hyper-V/WSL y `uvicorn` falla con `WinError 10013`. El repo usa 8001 como
> default (`.env.example`, fallback en `App.jsx`, READMEs). CORS acepta cualquier
> puerto de `localhost` para tolerar que Vite salte de puerto.