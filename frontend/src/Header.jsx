import './Header.css'

function VinylLogo() {
  return (
    <svg className="site-header__logo" viewBox="0 0 32 32" aria-hidden="true">
      <circle className="site-header__logo-disc" cx="16" cy="16" r="15" />
      <circle className="site-header__logo-groove" cx="16" cy="16" r="10.5" />
      <circle className="site-header__logo-groove" cx="16" cy="16" r="7" />
      <circle className="site-header__logo-label" cx="16" cy="16" r="4.5" />
      <circle className="site-header__logo-hole" cx="16" cy="16" r="1.4" />
    </svg>
  )
}

function Header() {
  return (
    <header className="site-header">
      <div className="site-header__inner">
        <div className="site-header__brand">
          <VinylLogo />
          <div>
            <span className="site-header__name">RecordShop AI</span>
            <span className="site-header__tagline">CDs and vinyl records with a built-in assistant</span>
          </div>
        </div>

        <nav className="site-header__nav">
          <a href="#catalogo">Catalog</a>
          <a href="#politicas">Shipping &amp; Returns</a>
        </nav>
      </div>
    </header>
  )
}

export default Header
