function Navbar() {
  return (
    <header className="navbar">
      <a className="brand" href="#top" aria-label="CityPulse home">
        <span className="brand-icon" aria-hidden="true">C</span>
        <span className="brand-copy"><strong>CityPulse</strong><small>Civic intelligence dashboard</small></span>
      </a>
      <div className="navbar-right"><span className="location"><span aria-hidden="true">⌖</span> Jaipur</span><span className="connection-status live-status"><span className="live-dot" aria-hidden="true" /> Live · Connected</span></div>
    </header>
  );
}
export default Navbar;
