import { forwardRef, useEffect, useImperativeHandle, useRef, useState } from 'react'
import './Chat.css'

const WELCOME_MESSAGE = {
  role: 'assistant',
  text: "Hi! I'm the RecordShop AI assistant. Ask me about the catalog, shipping, or returns.",
}

// Debe coincidir con el límite del backend (ver ChatRequest en main.py).
const MAX_LENGTH = 2000
const WARN_AT = 1800

const Chat = forwardRef(function Chat({ apiUrl }, ref) {
  const [messages, setMessages] = useState([WELCOME_MESSAGE])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const containerRef = useRef(null)
  const bottomRef = useRef(null)
  const textareaRef = useRef(null)

  useImperativeHandle(ref, () => ({
    // Lo usan las tarjetas de producto para precargar una pregunta y
    // llevar el foco al chat (útil sobre todo en mobile, donde el chat
    // queda debajo del catálogo en vez de al costado).
    askAbout(text) {
      setInput(text)
      containerRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
      textareaRef.current?.focus()
    },
  }))

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  useEffect(() => {
    // Foco automático al cargar y después de cada respuesta, para poder
    // seguir escribiendo sin tener que volver a hacer click en el input.
    if (!loading) textareaRef.current?.focus()
  }, [loading])

  useEffect(() => {
    // Auto-grow del textarea según el contenido, con una altura máxima.
    // overflow se mantiene oculto salvo que el contenido realmente supere
    // esa altura: si no, Windows a veces dibuja una scrollbar nativa de
    // 1px de más por redondeo, aunque el texto entre en una sola línea.
    const el = textareaRef.current
    if (!el) return
    el.style.height = 'auto'
    const needsScroll = el.scrollHeight > 120
    el.style.height = `${Math.min(el.scrollHeight, 120)}px`
    el.style.overflowY = needsScroll ? 'auto' : 'hidden'
  }, [input])

  async function sendMessage(e) {
    e?.preventDefault()
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
        throw new Error(data.detail ?? 'Unknown server error')
      }
      setMessages((prev) => [...prev, { role: 'assistant', text: data.reply }])
    } catch (err) {
      // Falló: sacamos el mensaje del historial y lo devolvemos al input,
      // así no hay que retipearlo para reintentar.
      setMessages((prev) => prev.slice(0, -1))
      setInput(text)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  function handleKeyDown(e) {
    // Enter envía, Shift+Enter agrega un salto de línea.
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  function clearChat() {
    setMessages([WELCOME_MESSAGE])
    setError(null)
  }

  return (
    <div className="chat" ref={containerRef}>
      <div className="chat__header">
        <span>Chat</span>
        <button
          type="button"
          className="chat__clear"
          onClick={clearChat}
          disabled={messages.length === 1}
        >
          Clear conversation
        </button>
      </div>

      <div className="chat__messages">
        {messages.map((m, i) => (
          <div key={i} className={`chat__row chat__row--${m.role}`}>
            {m.role === 'assistant' && (
              <span className="chat__avatar" aria-hidden="true">
                🎧
              </span>
            )}
            <div className={`chat__bubble chat__bubble--${m.role}`}>{m.text}</div>
          </div>
        ))}

        {loading && (
          <div className="chat__row chat__row--assistant">
            <span className="chat__avatar" aria-hidden="true">
              🎧
            </span>
            <div className="chat__bubble chat__bubble--assistant chat__bubble--loading">
              <span className="chat__typing-dot" />
              <span className="chat__typing-dot" />
              <span className="chat__typing-dot" />
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {error && (
        <div className="chat__error">
          <span>{error}</span>
          <button
            type="button"
            className="chat__error-dismiss"
            onClick={() => setError(null)}
            aria-label="Dismiss error"
          >
            ×
          </button>
        </div>
      )}

      <form className="chat__form" onSubmit={sendMessage}>
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value.slice(0, MAX_LENGTH))}
          onKeyDown={handleKeyDown}
          placeholder="Type your question… (Enter to send)"
          disabled={loading}
          rows={1}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          Send
        </button>
      </form>
      {input.length >= WARN_AT && (
        <p className="chat__counter">
          {input.length}/{MAX_LENGTH}
        </p>
      )}
    </div>
  )
})

export default Chat
