import './Header.css'

const STATUS_LABEL = {
  checking: 'verificando…',
  ok: 'conectado',
  error: 'sin conexión',
}

function Header({ backendStatus }) {
  return (
    <header className="site-header">
      <div className="site-header__brand">
        <span className="site-header__logo" aria-hidden="true">
          💿
        </span>
        <div>
          <span className="site-header__name">RecordShop AI</span>
          <span className="site-header__tagline">CDs y vinilos con asistente propio</span>
        </div>
      </div>

      <nav className="site-header__nav">
        <a href="#catalogo">Catálogo</a>
        <a href="#politicas">Envíos y devoluciones</a>
      </nav>

      <span className={`badge badge--${backendStatus}`}>
        <span className="badge__dot" />
        Backend {STATUS_LABEL[backendStatus]}
      </span>
    </header>
  )
}

export default Header
