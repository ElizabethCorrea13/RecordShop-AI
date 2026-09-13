import './Footer.css'

function Footer() {
  return (
    <footer id="politicas" className="site-footer">
      <div className="site-footer__grid">
        <div>
          <h4>Envíos</h4>
          <ul>
            <li>Estándar: 5-7 días hábiles — $1500</li>
            <li>Express: 2-3 días hábiles — $3500</li>
            <li>Gratis en compras +$15000</li>
            <li>Cobertura: todo el país</li>
          </ul>
        </div>
        <div>
          <h4>Devoluciones</h4>
          <ul>
            <li>30 días desde la recepción</li>
            <li>Producto sin usar, en empaque original</li>
            <li>Vinilos: sello de calidad no debe estar roto</li>
            <li>Oferta/liquidación: sin devolución, solo cambio</li>
          </ul>
        </div>
        <div>
          <h4>¿Dudas?</h4>
          <p className="site-footer__hint">
            Preguntale al asistente del chat sobre cualquier disco, envío o devolución.
          </p>
        </div>
      </div>

      <p className="site-footer__disclaimer">
        RecordShop AI — proyecto de portfolio. Catálogo, precios y políticas son
        ficticios; no se procesan pagos ni ventas reales.
      </p>
    </footer>
  )
}

export default Footer
