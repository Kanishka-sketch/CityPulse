function HealthScore() {
  return <section className="health-card" aria-labelledby="health-title"><div className="health-copy"><span className="eyebrow">JAIPUR · CITY HEALTH</span><h2 id="health-title">How is Jaipur doing right now?</h2><p>We’ll show a simple city health picture when current information is available.</p><div className="health-meta"><span className="status-pill neutral">Status unavailable</span><span className="updated-label">Updated just now · preview</span></div></div><div className="health-score-placeholder" aria-label="Health score not available"><span>—</span><small>/ 100</small></div></section>;
}
export default HealthScore;
