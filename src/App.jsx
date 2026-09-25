import { useEffect, useState } from "react";
import "./App.css";

import Navbar from "./components/Navbar";
import HealthScore from "./components/HealthScore";
import MetricCard from "./components/MetricCard";
import ActiveInsight from "./components/ActiveInsight";
import ConnectedSignals from "./components/ConnectedSignals";
import CityMap from "./components/CityMap";
import AnomalyList from "./components/AnomalyList";
import HowItWorks from "./components/HowItWorks";

import {
    getHealth,
    getInsight,
    getLatest,
    getAnomalies,
} from "./api";

function App() {
    const [health, setHealth] = useState(null);
    const [insight, setInsight] = useState(null);
    const [latest, setLatest] = useState(null);
    const [anomalies, setAnomalies] = useState(null);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function loadCityPulseData() {
            try {
                setLoading(true);
                setError(null);

                const [healthData, insightData, latestData, anomalyData] =
                    await Promise.all([
                        getHealth(),
                        getInsight(),
                        getLatest(),
                        getAnomalies(),
                    ]);

                setHealth(healthData);
                setInsight(insightData);
                setLatest(latestData);
                setAnomalies(anomalyData);
            } catch (err) {
                console.error("CityPulse API error:", err);
                setError("Unable to connect to CityPulse backend.");
            } finally {
                setLoading(false);
            }
        }

        loadCityPulseData();
    }, []);

    const signals = [
        {
            title: "Rain",
            detail: "Rainfall",
            icon: "☂",
            value: latest?.rain ?? "—",
            unit: "mm",
            interpretation:
                latest?.rain !== undefined
                    ? `${latest.rain} mm recorded`
                    : "Rainfall information unavailable",
        },
        {
            title: "Traffic",
            detail: "Traffic speed",
            icon: "↗",
            value:
                latest?.traffic_speed !== undefined
                    ? latest.traffic_speed.toFixed(1)
                    : "—",
            unit: "km/h",
            interpretation:
                latest?.traffic_speed !== undefined
                    ? "Current traffic speed"
                    : "Traffic information unavailable",
        },
        {
            title: "Citizen complaints",
            detail: "Reports from residents",
            icon: "▤",
            value: latest?.complaints ?? "—",
            unit: "reports",
            interpretation:
                latest?.complaints !== undefined
                    ? "Current reported complaints"
                    : "No updates available",
        },
        {
            title: "Air quality",
            detail: "Fine particles (PM2.5)",
            icon: "◌",
            value:
                latest?.pm25 !== undefined ? latest.pm25.toFixed(1) : "—",
            unit: "µg/m³",
            interpretation:
                latest?.pm25 !== undefined
                    ? "Current PM2.5 level"
                    : "Air quality unavailable",
        },
        {
            title: "Power",
            detail: "Outages",
            icon: "ϟ",
            value: latest?.outage_count ?? "—",
            unit: "events",
            interpretation:
                latest?.outage_count !== undefined
                    ? "Current reported outages"
                    : "Power information unavailable",
        },
    ];

    return (
        <div className="app">
            <Navbar />

            <main>
                <HealthScore data={health} loading={loading} />

                <section className="pulse-card" aria-labelledby="pulse-title">
                    <div className="pulse-icon" aria-hidden="true">
                        ◉
                    </div>

                    <div>
                        <span className="eyebrow">TODAY AT A GLANCE</span>

                        <h2 id="pulse-title">Today’s city pulse</h2>

                        <p>
                            {loading
                                ? "Getting the latest civic signals for Jaipur..."
                                : insight?.message ||
                                "Current civic conditions are being analyzed."}
                        </p>
                    </div>
                </section>

                <section
                    className="metrics-section"
                    aria-labelledby="signals-heading"
                >
                    <div className="section-heading">
                        <div>
                            <span className="eyebrow">
                                A QUICK LOOK AROUND THE CITY
                            </span>

                            <h2 id="signals-heading">
                                What’s happening around Jaipur?
                            </h2>
                        </div>

                        <span className="data-pending">
                            {loading ? "Updating..." : "Live · Connected"}
                        </span>
                    </div>

                    <div className="metrics">
                        {signals.map((signal) => (
                            <MetricCard
                                key={signal.title}
                                {...signal}
                            />
                        ))}
                    </div>
                </section>

                <div className="dashboard-grid">
                    <ActiveInsight
                        data={insight}
                        loading={loading}
                    />

                    <CityMap
                        data={anomalies}
                        latest={latest}
                        loading={loading}
                    />
                </div>

                <ConnectedSignals
                    data={insight}
                    loading={loading}
                />

                <AnomalyList
                    data={anomalies}
                    loading={loading}
                />

                <HowItWorks />
            </main>

            <footer className="footer-note">
                CityPulse <span>·</span> Jaipur civic dashboard
            </footer>

            {error && (
                <div className="api-error">
                    {error}
                </div>
            )}
        </div>
    );
}

export default App;