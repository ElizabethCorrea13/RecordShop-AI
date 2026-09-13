import { useEffect, useRef, useState } from 'react'
import Header from './Header'
import Footer from './Footer'
import ProductGrid from './ProductGrid'
import Chat from './Chat'
import './App.css'

// URL de la API. En desarrollo apunta al backend de FastAPI en localhost:8001.
// Se puede sobreescribir con la variable de entorno VITE_API_URL (ver .env.example).
const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8001'

function App() {
  // Estado del backend: 'checking' | 'ok' | 'error'. Se usa para habilitar el
  // chat y para mostrarle al usuario si el backend está disponible.
  const [backendStatus, setBackendStatus] = useState('checking')
  const chatRef = useRef(null)

  useEffect(() => {
    fetch(`${API_URL}/health`)
      .then((res) => (res.ok ? res.json() : Promise.reject(res)))
      .then((data) => setBackendStatus(data.status === 'ok' ? 'ok' : 'error'))
      .catch(() => setBackendStatus('error'))
  }, [])

  return (
    <div className="page">
      <Header />

      <div className="layout">
        <main className="layout__main">
          <p className="layout__intro">
            Curated vinyl records and CDs. Ask the assistant about any album,
            shipping, or returns.
          </p>
          <ProductGrid
            apiUrl={API_URL}
            onAskAbout={(text) => chatRef.current?.askAbout(text)}
          />
        </main>

        <aside className="layout__chat">
          {backendStatus === 'ok' ? (
            <Chat ref={chatRef} apiUrl={API_URL} />
          ) : (
            <p className="layout__placeholder">
              {backendStatus === 'checking'
                ? 'Connecting to the server…'
                : "The chat isn't available right now. Try again in a moment."}
            </p>
          )}
        </aside>
      </div>

      <Footer />
    </div>
  )
}

export default App
