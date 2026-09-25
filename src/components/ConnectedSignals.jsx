function ConnectedSignals({ data, loading }) {
    const correlations = data?.correlations || [];

    const names = {
        rain: "Rainfall",
        complaints: "Citizen complaints",
        outage_count: "Power outages",
        affected_customers: "Affected customers",
        traffic_speed: "Traffic speed",
        pm25: "Air quality",
    };

    if (loading) {
        return (
            <section className="panel correlations-panel">
                <div className="panel-heading">
                    <div>
                        <span className="eyebrow">
                            LOOKING AT THE BIGGER PICTURE
                        </span>
                        <h2>Why might these signals be connected?</h2>
                    </div>

                    <span className="status-pill neutral">
                        Updating...
                    </span>
                </div>
            </section>
        );
    }

    return (
        <section className="panel correlations-panel">

            <div className="panel-heading">
                <div>
                    <span className="eyebrow">
                        LOOKING AT THE BIGGER PICTURE
                    </span>

                    <h2>
                        Why might these signals be connected?
                    </h2>
                </div>

                <span className="status-pill neutral">
                    {correlations.length > 0
                        ? `${correlations.length} relationships`
                        : "No relationship"}
                </span>
            </div>


            {correlations.length > 0 ? (
                <>
                    <div className="connected-flow">

                        {correlations.slice(0, 3).map((item, index) => (
                            <div
                                className="connection-item"
                                key={`${item.signal_1}-${item.signal_2}`}
                            >

                                <div className="connection-signal">
                                    {names[item.signal_1] || item.signal_1}
                                </div>

                                <div className="connection-arrow">
                                    ↕
                                </div>

                                <div className="connection-signal">
                                    {names[item.signal_2] || item.signal_2}
                                </div>

                                <div className="connection-score">
                                    {Number(item.correlation).toFixed(2)}
                                </div>

                            </div>
                        ))}

                    </div>


                    <div className="connection-summary">

                        <span>
                            ◉
                        </span>

                        <p>
                            These signals showed measurable historical relationships in the recent data.
                        </p>

                    </div>


                    <div className="honesty-note">
                        Correlation shows signals changing together;
                        it does not confirm that one caused the other.
                    </div>

                </>
            ) : (
                <div className="relationship-empty">
                    <span>↔</span>

                    <div>
                        <strong>No strong relationship detected</strong>

                        <p>
                            We'll show related changes when the available
                            signals move together.
                        </p>
                    </div>
                </div>
            )}

        </section>
    );
}

export default ConnectedSignals;
