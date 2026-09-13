import './Footer.css'

function Footer() {
  return (
    <footer id="politicas" className="site-footer">
      <div className="site-footer__grid">
        <div>
          <h4>Shipping</h4>
          <ul>
            <li>Standard: 5-7 business days — $1500</li>
            <li>Express: 2-3 business days — $3500</li>
            <li>Free on orders over $15000</li>
            <li>Coverage: nationwide</li>
          </ul>
        </div>
        <div>
          <h4>Returns</h4>
          <ul>
            <li>30 days from receipt</li>
            <li>Item must be unused, in original packaging</li>
            <li>Vinyl records: quality seal must not be broken</li>
            <li>Sale/clearance items: no returns, exchange only</li>
          </ul>
        </div>
        <div>
          <h4>Questions?</h4>
          <p className="site-footer__hint">
            Ask the chat assistant about any album, shipping, or returns.
          </p>
        </div>
      </div>

      <p className="site-footer__disclaimer">
        RecordShop AI — a portfolio project. Catalog, prices, and policies are
        fictional; no real payments or sales are processed.
      </p>
    </footer>
  )
}

export default Footer
