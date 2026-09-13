import { useEffect, useState } from 'react'
import './ProductGrid.css'

function ProductCover({ product }) {
  const [failed, setFailed] = useState(false)

  if (product.cover && !failed) {
    return (
      <img
        className="product-card__cover-img"
        src={product.cover}
        alt={`Cover art for ${product.name}`}
        loading="lazy"
        onError={() => setFailed(true)}
      />
    )
  }

  // Respaldo si el álbum no tiene portada o la URL falla: mismo bloque de
  // color de antes, para que la tarjeta nunca quede rota.
  return (
    <div className={`product-card__cover product-card__cover--${slug(product.genre)}`}>
      {product.format === 'vinyl' ? '💿' : '📀'}
    </div>
  )
}

const CURRENCY = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 0,
})

// A partir de cuántas unidades dejamos de marcar "casi sin stock".
const LOW_STOCK_THRESHOLD = 5

function stockStatus(stock) {
  if (stock === 0) return 'out'
  if (stock <= LOW_STOCK_THRESHOLD) return 'low'
  return 'ok'
}

function ProductGrid({ apiUrl, onAskAbout }) {
  const [products, setProducts] = useState([])
  const [status, setStatus] = useState('loading') // loading | ok | error
  const [genreFilter, setGenreFilter] = useState('all')

  useEffect(() => {
    fetch(`${apiUrl}/catalog`)
      .then((res) => (res.ok ? res.json() : Promise.reject(res)))
      .then((data) => {
        setProducts(data)
        setStatus('ok')
      })
      .catch(() => setStatus('error'))
  }, [apiUrl])

  const genres = ['all', ...new Set(products.map((p) => p.genre))]
  const visible =
    genreFilter === 'all' ? products : products.filter((p) => p.genre === genreFilter)

  if (status === 'loading') {
    return <p className="products__status">Loading catalog…</p>
  }

  if (status === 'error') {
    return <p className="products__status products__status--error">Couldn't load the catalog.</p>
  }

  return (
    <section id="catalogo" className="products">
      <div className="products__filters">
        {genres.map((g) => (
          <button
            key={g}
            type="button"
            className={`products__filter ${genreFilter === g ? 'products__filter--active' : ''}`}
            onClick={() => setGenreFilter(g)}
          >
            {g}
          </button>
        ))}
      </div>

      <div className="products__grid">
        {visible.map((p) => (
          <article key={p.id} className="product-card">
            <ProductCover product={p} />
            <div className="product-card__body">
              <h3>{p.name}</h3>
              <p className="product-card__artist">{p.artist}</p>
              <p className="product-card__meta">
                <span className={`product-card__format product-card__format--${p.format}`}>
                  {p.format === 'vinyl' ? 'Vinyl' : 'CD'}
                </span>{' '}
                · {p.genre}
              </p>
              <div className="product-card__footer">
                <span className="product-card__price">{CURRENCY.format(p.price)}</span>
                <span className={`product-card__stock product-card__stock--${stockStatus(p.stock)}`}>
                  {p.stock === 0 ? 'Out of stock' : `${p.stock} in stock`}
                </span>
              </div>
              <button
                type="button"
                className="product-card__ask"
                onClick={() => onAskAbout(`Do you have ${p.name} by ${p.artist}?`)}
              >
                Ask the assistant
              </button>
            </div>
          </article>
        ))}
      </div>
    </section>
  )
}

function slug(genre) {
  return genre.replace(/\s+/g, '-')
}

export default ProductGrid
