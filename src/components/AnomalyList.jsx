function AnomalyList({ data, loading }) {
    const anomalies = data?.anomalies || [];

    const formatTime = (timestamp) => {
        if (!timestamp) return "Time unavailable";

        return new Date(timestamp).toLocaleString("en-IN", {
            day: "2-digit",
            month: "short",
            hour: "2-digit",
            minute: "2-digit",
        });
    };

    const getSignal = (item) => {
        if (item.traffic_speed < 35) {
            return {
                title: "Traffic speed dropped",
                type: "traffic",
                icon: "↘",
            };
        }

        if (item.rain >= 1) {
            return {
                title: "Elevated rainfall detected",
                type: "weather",
                icon: "☂",
            };
        }

        if (item.complaints >= 18) {
            return {
                title: "Complaint activity increased",
                type: "complaints",
                icon: "▤",
            };
        }

        if (item.pm25 >= 60) {
            return {
                title: "Air quality changed",
                type: "air",
                icon: "◌",
            };
        }

        if (item.outage_count >= 3) {
            return {
                title: "Multiple power outages",
                type: "power",
                icon: "ϟ",
            };
        }

        return {
            title: "Unusual civic pattern detected",
            type: "general",
            icon: "!",
        };
    };

    return (
        <section
            className="panel anomaly-panel"
            aria-labelledby="anomaly-title"
        >
            <div className="panel-heading">
                <div>
                    <span className="eyebrow">JAIPUR, RECENTLY</span>

                    <h2 id="anomaly-title">What changed recently?</h2>
                </div>

                <span className="status-pill neutral">
                    {loading ? "Updating..." : `${data?.count || 0} recent`}
                </span>
            </div>

            {loading ? (
                <div className="anomaly-empty">
                    <span>◷</span>
                    <div>
                        <strong>Checking recent activity...</strong>
                        <p>CityPulse is analyzing recent civic signals.</p>
                    </div>
                </div>
            ) : anomalies.length === 0 ? (
                <div className="anomaly-empty">
                    <span>✓</span>
                    <div>
                        <strong>No unusual activity detected</strong>
                        <p>Recent civic signals are within normal patterns.</p>
                    </div>
                </div>
            ) : (
                <div className="anomaly-list">
                    {anomalies.slice(0, 5).map((item, index) => {
                        const signal = getSignal(item);

                        return (
                            <article
                                className={`anomaly-item anomaly-${signal.type}`}
                                key={index}
                            >
                                <div className="anomaly-icon">
                                    {signal.icon}
                                </div>

                                <div className="anomaly-content">
                                    <div className="anomaly-title-row">
                                        <strong>{signal.title}</strong>

                                        <span className="anomaly-badge">
                                            ANOMALY
                                        </span>
                                    </div>

                                    <p>
                                        {formatTime(item.timestamp)}
                                        <span> · </span>
                                        Jaipur
                                    </p>
                                </div>

                                <div className="anomaly-arrow">→</div>
                            </article>
                        );
                    })}
                </div>
            )}
        </section>
    );
}

export default AnomalyList;