function ActiveInsight({ data, loading }) {
    const status = data?.status || "normal";

    const statusLabel =
        status === "warning"
            ? "Possible disruption"
            : status === "watch"
                ? "Needs attention"
                : "Normal";

    const statusClass =
        status === "warning"
            ? "critical"
            : status === "watch"
                ? "watch"
                : "healthy";

    const reasons = data?.reasons || [];

    const correlations = data?.correlations || [];

    return (
        <section
            className="panel insight-panel"
            aria-labelledby="insight-title"
        >
            <div className="panel-heading">
                <div>
                    <span className="eyebrow">WHY ENGINE</span>
                    <h2 id="insight-title">What should you know?</h2>
                </div>

                <span className={`status-pill ${statusClass}`}>
                    {loading ? "Updating..." : statusLabel}
                </span>
            </div>

            <div className="empty-state">
                <span className="empty-mark" aria-hidden="true">
                    ◎
                </span>

                <div>
                    <h3>
                        {loading
                            ? "Analyzing Jaipur"
                            : data?.message || "Civic conditions appear normal"}
                    </h3>

                    <p>
                        {loading
                            ? "We're checking the latest civic signals."
                            : reasons.length > 0
                                ? reasons.join(" · ")
                                : "No unusual conditions detected right now."}
                    </p>
                    {!loading && status === "normal" && (
                        <p className="status-clarification">
                            Latest observation is normal; recent anomalies are shown below.
                        </p>
                    )}
                </div>
            </div>
            {correlations.length > 0 && (
                <div className="contributing-preview">
                    {correlations.slice(0, 3).map((item, index) => {
                        const names = {
                            rain: "Rainfall",
                            complaints: "Complaints",
                            outage_count: "Power outages",
                            affected_customers: "Affected customers",
                            traffic_speed: "Traffic",
                            pm25: "Air quality",
                        };

                        return (
                            <span key={index}>
                                {names[item.signal_1] || item.signal_1}
                                <b> ↕ </b>
                                {names[item.signal_2] || item.signal_2}
                            </span>
                        );
                    })}
                </div>
            )}
            <div className="honesty-note">
                Observed relationships are not confirmed causes.
            </div>
        </section>
    );
}

export default ActiveInsight;
