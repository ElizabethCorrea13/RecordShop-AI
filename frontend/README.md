# RecordShop AI — Frontend

Interfaz de chat en React, generada con [Vite](https://vite.dev/).

## Requisitos

- Node.js 20+ (probado con Node 24)

## Cómo correrlo localmente

```bash
cd frontend
npm install
cp .env.example .env   # ajustar VITE_API_URL si el backend no está en localhost:8001
npm run dev
```

En PowerShell, en vez de `cp` usá `Copy-Item .env.example .env`.

La app queda en http://localhost:5173 y hace un ping a `GET /health` del backend
para mostrar si la conexión funciona.

## Scripts

- `npm run dev` — servidor de desarrollo con hot reload
- `npm run build` — build de producción en `dist/`
- `npm run preview` — sirve el build de producción para probarlo
- `npm run lint` — linter (oxlint)
