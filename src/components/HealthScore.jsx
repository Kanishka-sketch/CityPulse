function HealthScore({ data, loading }) {
  const score = data?.health_score;
  const status = data?.status || "Unavailable";

  const statusClass =
    status === "Healthy"
      ? "healthy"
      : status === "Watch"
        ? "watch"
        : status === "Critical"
          ? "critical"
          : "neutral";

  return (
    <section className="health-card" aria-labelledby="health-title">
      <div className="health-copy">
        <span className="eyebrow">JAIPUR · CITY HEALTH</span>

        <h2 id="health-title">How is Jaipur doing right now?</h2>

        <p>
          {loading
            ? "Getting the latest civic health signals..."
            : "A simple city health picture based on current civic conditions."}
        </p>

        <div className="health-meta">
          <span className={`status-pill ${statusClass}`}>
            {loading ? "Updating..." : status}
          </span>

          <span className="updated-label">
            {loading ? "Updating..." : "Updated just now · live"}
          </span>
        </div>
      </div>

      <div
        className="health-score-placeholder"
        aria-label={`Health score ${score ?? "not available"}`}
      >
        <span>{score !== undefined ? score : "—"}</span>
        <small>/ 100</small>
      </div>
    </section>
  );
}

export default HealthScore;