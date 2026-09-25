function MetricCard({
    title,
    detail,
    icon,
    value,
    unit,
    interpretation,
}) {
    return (
        <article className="metric-card" tabIndex="0">
            <div className="metric-top">
                <span className="metric-icon" aria-hidden="true">
                    {icon}
                </span>

                <span className="metric-title">{title}</span>
            </div>

            <p className="metric-detail">{detail}</p>

            <div className="metric-value">
                <span>{value !== undefined && value !== null ? value : "—"}</span>
                <small>{unit}</small>
            </div>

            <span className="metric-waiting">
                {interpretation}
            </span>
        </article>
    );
}

export default MetricCard;