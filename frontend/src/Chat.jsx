import { useEffect, useRef, useState } from 'react'
import './Chat.css'

const WELCOME_MESSAGE = {
  role: 'assistant',
  text: '¡Hola! Soy el asistente de RecordShop AI. Preguntame sobre el catálogo, envíos o devoluciones.',
}

function Chat({ apiUrl }) {
  const [messages, setMessages] = useState([WELCOME_MESSAGE])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  async function sendMessage(e) {
    e.preventDefault()
    const text = input.trim()
    if (!text || loading) return

    setMessages((prev) => [...prev, { role: 'user', text }])
    setInput('')
    setLoading(true)
    setError(null)

    try {
      const res = await fetch(`${apiUrl}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      })
      const data = await res.json()
      if (!res.ok) {
        // El backend manda el detalle del error en `detail` (ver backend/main.py)
        throw new Error(data.detail ?? 'Error desconocido del servidor')
      }
      setMessages((prev) => [...prev, { role: 'assistant', text: data.reply }])
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chat">
      <div className="chat__messages">
        {messages.map((m, i) => (
          <div key={i} className={`chat__bubble chat__bubble--${m.role}`}>
            {m.text}
          </div>
        ))}
        {loading && (
          <div className="chat__bubble chat__bubble--assistant chat__bubble--loading">
            escribiendo…
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {error && <p className="chat__error">{error}</p>}

      <form className="chat__form" onSubmit={sendMessage}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Escribí tu consulta…"
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          Enviar
        </button>
      </form>
    </div>
  )
}

export default Chat
