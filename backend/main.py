"""
RecordShop AI — API backend.

Por ahora sólo expone un endpoint de health-check para verificar que el
servidor levanta bien. La lógica del chatbot y la integración con Gemini
se agregan más adelante.

Cómo correrlo (desde la carpeta backend/, con el venv activado):
    uvicorn main:app --reload --port 8001
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RecordShop AI API", version="0.1.0")

# CORS = Cross-Origin Resource Sharing. El navegador bloquea por defecto que
# una página servida desde un origen (ej. http://localhost:5173, donde corre
# el frontend) haga fetch a otro origen (esta API en el puerto 8001). Este
# middleware le dice a FastAPI que agregue las cabeceras que autorizan al
# frontend a llamar a la API.
#
# Se usa una regex para aceptar cualquier puerto de localhost/127.0.0.1: en
# desarrollo Vite arranca en 5173 pero si ese puerto está ocupado salta al
# 5174, 5175, etc. Para producción esto habrá que restringirlo al dominio real.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    """Health-check simple: sirve para monitoreo y para probar el deploy."""
    return {"status": "ok"}
