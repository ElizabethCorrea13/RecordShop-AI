import { useEffect, useState } from 'react'
import Chat from './Chat'
import './App.css'

// URL de la API. En desarrollo apunta al backend de FastAPI en localhost:8001.
// Se puede sobreescribir con la variable de entorno VITE_API_URL (ver .env.example).
const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8001'

const STATUS_LABEL = {
  checking: 'verificando…',
  ok: 'conectado',
  error: 'sin conexión',
}

function App() {
  // Estado del backend: 'checking' | 'ok' | 'error'. Se usa para habilitar el
  // chat y para mostrarle al usuario si el backend está disponible.
  const [backendStatus, setBackendStatus] = useState('checking')

  useEffect(() => {
    fetch(`${API_URL}/health`)
      .then((res) => (res.ok ? res.json() : Promise.reject(res)))
      .then((data) => setBackendStatus(data.status === 'ok' ? 'ok' : 'error'))
      .catch(() => setBackendStatus('error'))
  }, [])

  return (
    <main className="app">
      <header className="app__header">
        <div className="app__title-row">
          <span className="app__logo" aria-hidden="true">
            💿
          </span>
          <div>
            <h1>RecordShop AI</h1>
            <p className="app__subtitle">
              Chatbot de soporte para una tienda de CDs y vinilos
            </p>
          </div>
        </div>

        <span className={`badge badge--${backendStatus}`}>
          <span className="badge__dot" />
          Backend {STATUS_LABEL[backendStatus]}
        </span>
      </header>

      {backendStatus === 'ok' ? (
        <Chat apiUrl={API_URL} />
      ) : (
        <p className="app__placeholder">
          {backendStatus === 'checking'
            ? 'Conectando con el servidor…'
            : 'El chat necesita que el backend esté corriendo (ver estado arriba).'}
        </p>
      )}
    </main>
  )
}

export default App
