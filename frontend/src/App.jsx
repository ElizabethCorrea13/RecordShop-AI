import { useEffect, useState } from 'react'
import Chat from './Chat'
import './App.css'

// URL de la API. En desarrollo apunta al backend de FastAPI en localhost:8001.
// Se puede sobreescribir con la variable de entorno VITE_API_URL (ver .env.example).
const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8001'

function App() {
  // Estado del backend: 'checking' | 'ok' | 'error'
  // Por ahora el frontend sólo hace un ping a /health para verificar que
  // la conexión front <-> back funciona. El chat y la integración con
  // Gemini se agregan más adelante.
  const [backendStatus, setBackendStatus] = useState('checking')

  useEffect(() => {
    fetch(`${API_URL}/health`)
      .then((res) => (res.ok ? res.json() : Promise.reject(res)))
      .then((data) => setBackendStatus(data.status === 'ok' ? 'ok' : 'error'))
      .catch(() => setBackendStatus('error'))
  }, [])

  return (
    <main className="app">
      <h1>RecordShop AI</h1>
      <p className="subtitle">
        Chatbot de soporte para una tienda de CDs y vinilos.
      </p>

      <p className={`status status--${backendStatus}`}>
        Backend:{' '}
        {backendStatus === 'checking' && 'verificando…'}
        {backendStatus === 'ok' && 'conectado'}
        {backendStatus === 'error' && 'sin conexión'}
      </p>

      {backendStatus === 'ok' ? (
        <Chat apiUrl={API_URL} />
      ) : (
        <p className="placeholder">
          El chat necesita que el backend esté corriendo (ver estado arriba).
        </p>
      )}
    </main>
  )
}

export default App
