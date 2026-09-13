import { useEffect, useState } from 'react'
import './ProductGrid.css'

function ProductCover({ product }) {
  const [failed, setFailed] = useState(false)

  if (product.cover && !failed) {
    return (
      <img
        className="product-card__cover-img"
        src={product.cover}
        alt={`Portada de ${product.name}`}
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

const CURRENCY = new Intl.NumberFormat('es-AR', {
  style: 'currency',
  currency: 'ARS',
  maximumFractionDigits: 0,
})

function ProductGrid({ apiUrl, onAskAbout }) {
  const [products, setProducts] = useState([])
  const [status, setStatus] = useState('loading') // loading | ok | error
  const [genreFilter, setGenreFilter] = useState('todos')

  useEffect(() => {
    fetch(`${apiUrl}/catalog`)
      .then((res) => (res.ok ? res.json() : Promise.reject(res)))
      .then((data) => {
        setProducts(data)
        setStatus('ok')
      })
      .catch(() => setStatus('error'))
  }, [apiUrl])

  const genres = ['todos', ...new Set(products.map((p) => p.genre))]
  const visible =
    genreFilter === 'todos' ? products : products.filter((p) => p.genre === genreFilter)

  if (status === 'loading') {
    return <p className="products__status">Cargando catálogo…</p>
  }

  if (status === 'error') {
    return <p className="products__status products__status--error">No se pudo cargar el catálogo.</p>
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
                {p.format === 'vinyl' ? 'Vinilo' : 'CD'} · {p.genre}
              </p>
              <div className="product-card__footer">
                <span className="product-card__price">{CURRENCY.format(p.price)}</span>
                {p.stock === 0 ? (
                  <span className="product-card__stock product-card__stock--out">Agotado</span>
                ) : (
                  <span className="product-card__stock">{p.stock} en stock</span>
                )}
              </div>
              <button
                type="button"
                className="product-card__ask"
                onClick={() => onAskAbout(`Tienen ${p.name} de ${p.artist}?`)}
              >
                Preguntarle al asistente
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
