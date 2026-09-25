import L from "leaflet";
import {
    MapContainer,
    TileLayer,
    Marker,
    Popup,
    Circle,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";

function CityMap({ data, latest, loading }) {
    const anomalies = data?.anomalies || [];

    const getSignal = (item) => {
        if (item.traffic_speed < 35) return "Traffic speed dropped";
        if (item.rain >= 1) return "Elevated rainfall detected";
        if (item.complaints >= 18) return "Complaint activity increased";
        if (item.pm25 >= 60) return "Air quality changed";
        if (item.outage_count >= 3) return "Multiple power outages";
        return "Unusual civic pattern";
    };

    const evidenceSignals = [
        { key: "outage_count", test: (value) => value >= 3, label: "Multiple power outages" },
        { key: "rain", test: (value) => value >= 1, label: "Elevated rainfall" },
        { key: "complaints", test: (value) => value >= 18, label: "Complaint activity increased" },
        { key: "traffic_speed", test: (value) => value < 35, label: "Traffic speed dropped" },
        { key: "pm25", test: (value) => value >= 60, label: "Air quality changed" },
    ];

    const evidenceFields = [
        ["traffic_speed", "Traffic speed", " km/h"],
        ["complaints", "Complaints", ""],
        ["rain", "Rainfall", " mm"],
        ["pm25", "PM2.5", ""],
        ["outage_count", "Power outages", ""],
    ];

    const formatEvidenceValues = (items, key, unit) => {
        const values = [...new Set(items
            .map((item) => item[key])
            .filter((value) => value !== null && value !== undefined && value !== "")
            .map((value) => `${value}${unit}`))];
        return values.length ? values.join(", ") : "—";
    };

    const isAnomaly = (item) =>
        item.is_anomaly === true || item.is_anomaly === 1 ||
        item.is_anomaly === "1" || item.is_anomaly === "true";

    // -----------------------------------------
    // GROUP ANOMALIES BY LOCATION
    // -----------------------------------------
    const groups = {};

    anomalies.forEach((item) => {
        const lat = Number(item.latitude);
        const lon = Number(item.longitude);

        if (!Number.isFinite(lat) || !Number.isFinite(lon)) return;

        const key = `${lat.toFixed(6)},${lon.toFixed(6)}`;

        if (!groups[key]) {
            groups[key] = {
                lat,
                lon,
                items: [],
            };
        }

        groups[key].items.push(item);
    });

    const anomalyGroups = Object.values(groups);

    // -----------------------------------------
    // ANOMALY COUNT MARKER
    // -----------------------------------------
    const createClusterIcon = (count) =>
        L.divIcon({
            className: "anomaly-cluster-icon",
            html: `<div>${count}</div>`,
            iconSize: [48, 48],
            iconAnchor: [24, 24],
        });

    // -----------------------------------------
    // CURRENT NORMAL MARKER
    // -----------------------------------------
    const createNormalIcon = () =>
        L.divIcon({
            className: "current-normal-icon",
            html: `<div>✓</div>`,
            iconSize: [30, 30],
            iconAnchor: [15, 15],
        });

    return (
        <section
            className="panel map-panel"
            aria-labelledby="map-title"
        >

            {/* HEADER */}
            <div className="panel-heading">
                <div>
                    <span className="eyebrow">
                        JAIPUR AT A GLANCE
                    </span>

                    <h2 id="map-title">
                        Where is something unusual happening?
                    </h2>
                </div>

                <span className="status-pill neutral">
                    {loading
                        ? "Updating..."
                        : `${anomalies.length} anomalies`}
                </span>
            </div>


            {/* LEGEND */}
            <div
                className="map-legend"
                aria-label="Map legend"
            >
                <span>
                    <i className="legend-dot red" />
                    Anomaly detected
                </span>

                <span>
                    <i className="legend-dot amber" />
                    Needs attention
                </span>

                <span>
                    <i className="legend-dot green" />
                    Normal
                </span>
            </div>


            {/* MAP */}
            <div className="map-wrapper">

                <MapContainer
                    center={[26.9124, 75.7873]}
                    zoom={12}
                    scrollWheelZoom={false}
                    className="city-map"
                >

                    <TileLayer
                        attribution="&copy; OpenStreetMap contributors"
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    />


                    {/* =========================================
                        ANOMALY / CIVIC IMPACT ZONES
                    ========================================== */}

                    {anomalyGroups.map((group, index) => {

                        const signalCounts = {};

                        group.items.forEach((item) => {
                            const signal = getSignal(item);

                            signalCounts[signal] =
                                (signalCounts[signal] || 0) + 1;
                        });


                        const topSignals = Object.entries(signalCounts)
                            .sort((a, b) => b[1] - a[1])
                            .slice(0, 4);

                        const whyFlagged = [...new Set(group.items.flatMap((item) =>
                            evidenceSignals
                                .filter(({ key, test }) => {
                                    const value = Number(item[key]);
                                    return item[key] !== null && item[key] !== "" && Number.isFinite(value) && test(value);
                                })
                                .map(({ label }) => label)
                        ))];
                        const anomalyDetected = group.items.some(isAnomaly);
                        const availableCorrelations = Array.isArray(data?.correlations)
                            ? data.correlations
                            : [];


                        // -------------------------------------
                        // IMPACT RADIUS
                        // More anomalies = larger visual zone
                        // -------------------------------------

                        const intensity = Math.min(
                            group.items.length,
                            20
                        );

                        const impactRadius =
                            600 + intensity * 45;


                        return (
                            <div key={`zone-${index}`}>

                                {/* --------------------------------
                                    GREEN BASELINE ZONE
                                --------------------------------- */}

                                <Circle
                                    center={[
                                        group.lat,
                                        group.lon,
                                    ]}
                                    radius={impactRadius * 1.45}
                                    pathOptions={{
                                        color: "#55d6be",
                                        fillColor: "#55d6be",
                                        fillOpacity: 0.045,
                                        weight: 1,
                                        opacity: 0.28,
                                    }}
                                />


                                {/* --------------------------------
                                    YELLOW MONITORING ZONE
                                --------------------------------- */}

                                <Circle
                                    center={[
                                        group.lat,
                                        group.lon,
                                    ]}
                                    radius={impactRadius}
                                    pathOptions={{
                                        color: "#ffd166",
                                        fillColor: "#ffd166",
                                        fillOpacity: 0.07,
                                        weight: 1,
                                        opacity: 0.4,
                                    }}
                                />


                                {/* --------------------------------
                                    ORANGE ATTENTION ZONE
                                --------------------------------- */}

                                <Circle
                                    center={[
                                        group.lat,
                                        group.lon,
                                    ]}
                                    radius={impactRadius * 0.68}
                                    pathOptions={{
                                        color: "#ff9f43",
                                        fillColor: "#ff9f43",
                                        fillOpacity: 0.10,
                                        weight: 1.5,
                                        opacity: 0.5,
                                    }}
                                />


                                {/* --------------------------------
                                    RED CORE ANOMALY ZONE
                                --------------------------------- */}

                                <Circle
                                    center={[
                                        group.lat,
                                        group.lon,
                                    ]}
                                    radius={impactRadius * 0.38}
                                    pathOptions={{
                                        color: "#ff5d5d",
                                        fillColor: "#ff5d5d",
                                        fillOpacity: 0.17,
                                        weight: 2,
                                        opacity: 0.7,
                                    }}
                                />


                                {/* --------------------------------
                                    ANOMALY COUNT
                                --------------------------------- */}

                                <Marker
                                    position={[
                                        group.lat,
                                        group.lon,
                                    ]}
                                    icon={createClusterIcon(
                                        group.items.length
                                    )}
                                >

                                    <Popup
                                        className="evidence-popup"
                                        minWidth={window.innerWidth <= 650 ? 280 : 380}
                                        maxWidth={420}
                                        autoPan
                                        autoPanPadding={[24, 24]}
                                        keepInView
                                    >

                                        <div
                                            style={{
                                                minWidth: window.innerWidth <= 650 ? "260px" : "380px",
                                            }}
                                        >

                                            <strong
                                                style={{
                                                    fontSize: "15px",
                                                }}
                                            >
                                                {group.items.length} anomalies
                                                detected
                                            </strong>


                                            <p
                                                style={{
                                                    margin: "7px 0",
                                                }}
                                            >
                                                🔴{" "}
                                                <strong>
                                                    Civic impact zone
                                                </strong>
                                            </p>


                                            <section className="evidence-trail">
                                                <strong className="evidence-title">Evidence Trail</strong>

                                                <div className="evidence-scroll">
                                                    <div className="evidence-block">
                                                        <span className="evidence-label">WHY FLAGGED?</span>
                                                        {whyFlagged.length ? (
                                                            <ul className="evidence-reasons">
                                                                {whyFlagged.map((signal) => <li key={signal}>{signal}</li>)}
                                                            </ul>
                                                        ) : <span className="evidence-value">—</span>}
                                                    </div>

                                                    <div className="evidence-values">
                                                        {evidenceFields.map(([key, label, unit]) => (
                                                            <div className="evidence-row" key={key}>
                                                                <span>{label}</span>
                                                                <strong>{formatEvidenceValues(group.items, key, unit)}</strong>
                                                            </div>
                                                        ))}
                                                    </div>

                                                    <div className="evidence-block">
                                                        <span className="evidence-label">ML SIGNAL</span>
                                                        <span className="evidence-value">
                                                            {anomalyDetected ? "Isolation Forest: Anomaly detected" : "—"}
                                                        </span>
                                                    </div>

                                                    <div className="evidence-block">
                                                        <span className="evidence-label">HISTORICAL RELATIONSHIP</span>
                                                        {availableCorrelations.length ? (
                                                            <ul className="evidence-reasons">
                                                                {availableCorrelations.map((item, correlationIndex) => (
                                                                    <li key={`${item.signal_1}-${item.signal_2}-${correlationIndex}`}>
                                                                        {item.signal_1} ↕ {item.signal_2}
                                                                        {item.correlation !== undefined && ` · ${item.correlation}`}
                                                                    </li>
                                                                ))}
                                                            </ul>
                                                        ) : <span className="evidence-value">available in Why Engine</span>}
                                                    </div>

                                                    <p className="evidence-disclaimer">
                                                        These signals are evidence of unusual activity, not proof of cause.
                                                    </p>
                                                </div>
                                            </section>


                                            <details className="evidence-map-details">
                                                <summary>Map and location details</summary>
                                                <strong>Detected signals:</strong>
                                                <ul>
                                                    {topSignals.map(([signal, count]) => (
                                                        <li key={signal}>{signal} <strong>({count})</strong></li>
                                                    ))}
                                                </ul>
                                                <p>
                                                    🟢 Green = normal baseline<br />
                                                    🟡 Yellow = monitoring zone<br />
                                                    🟠 Orange = attention zone<br />
                                                    🔴 Red = anomaly core
                                                </p>
                                                <small>
                                                    Estimated visual impact radius<br />
                                                    Coordinates: {group.lat.toFixed(4)}, {group.lon.toFixed(4)}
                                                </small>
                                            </details>

                                        </div>

                                    </Popup>

                                </Marker>

                            </div>
                        );
                    })}


                    {/* =========================================
                        CURRENT NORMAL CONDITION
                    ========================================== */}

                    {latest &&
                        Number.isFinite(
                            Number(latest.latitude)
                        ) &&
                        Number.isFinite(
                            Number(latest.longitude)
                        ) && (

                            <Marker
                                position={[
                                    Number(latest.latitude),
                                    Number(latest.longitude),
                                ]}
                                icon={createNormalIcon()}
                            >

                                <Popup>

                                    <div
                                        style={{
                                            minWidth: "190px",
                                        }}
                                    >

                                        <strong>
                                            Current CityPulse
                                        </strong>

                                        <p
                                            style={{
                                                margin: "7px 0",
                                            }}
                                        >
                                            🟢{" "}
                                            <strong>
                                                Current conditions normal
                                            </strong>
                                        </p>

                                        <p
                                            style={{
                                                fontSize: "12px",
                                                margin: 0,
                                            }}
                                        >
                                            The latest observation is
                                            currently within normal
                                            conditions.
                                        </p>

                                    </div>

                                </Popup>

                            </Marker>

                        )}

                </MapContainer>


                {/* EMPTY STATE */}

                {!loading && anomalies.length === 0 && (
                    <div className="map-empty">

                        <span>⌖</span>

                        <p>
                            No unusual activity detected right now.
                        </p>

                    </div>
                )}


                {/* MAP CREDIT */}

                <div className="map-credit">
                    Map data © OpenStreetMap
                </div>

            </div>

        </section>
    );
}

export default CityMap;
