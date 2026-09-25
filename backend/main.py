from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from services.insights import generate_insight
from services.health_score import calculate_health_score


# -----------------------------------
# App
# -----------------------------------

app = FastAPI(
    title="CityPulse API",
    description="Live Civic Health Dashboard API",
    version="1.0.0"
)


# -----------------------------------
# CORS
# -----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------
# Data
# -----------------------------------

DATA_FILE = "data/citypulse_anomalies.csv"


# -----------------------------------
# Root
# -----------------------------------

@app.get("/")
def root():

    return {
        "project": "CityPulse",
        "status": "running",
        "message": "CityPulse API is live"
    }


# -----------------------------------
# Health Score
# -----------------------------------

@app.get("/api/health")
def health():

    return calculate_health_score()


# -----------------------------------
# Why Engine
# -----------------------------------

@app.get("/api/insight")
def insight():

    return generate_insight()


# -----------------------------------
# Latest Civic Data
# -----------------------------------

@app.get("/api/latest")
def latest():

    df = pd.read_csv(DATA_FILE)

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    row = df.sort_values(
        "timestamp"
    ).iloc[-1]

    return {
        "timestamp": str(row["timestamp"]),
        "latitude": float(row["latitude"]),
        "longitude": float(row["longitude"]),

        "rain": float(row["rain"]),
        "pm25": float(row["pm25"]),
        "pm10": float(row["pm10"]),
        "no2": float(row["no2"]),
        "o3": float(row["o3"]),

        "traffic_speed": float(
            row["traffic_speed"]
        ),

        "complaints": int(
            row["complaints"]
        ),

        "outage_count": int(
            row["outage_count"]
        ),

        "affected_customers": int(
            row["affected_customers"]
        ),

        "outage_duration_min": float(
            row["outage_duration_min"]
        ),

        "is_anomaly": bool(
            row["is_anomaly"]
        ),

        "anomaly_score": float(
            row["anomaly_score"]
        )
    }


# -----------------------------------
# Anomalies
# -----------------------------------

@app.get("/api/anomalies")
def anomalies():

    df = pd.read_csv(DATA_FILE)

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    anomaly_df = df[
        df["is_anomaly"] == True
    ].copy()

    anomaly_df = anomaly_df.sort_values(
        "timestamp",
        ascending=False
    ).head(20)

    records = []

    for _, row in anomaly_df.iterrows():

        records.append({
            "timestamp": str(row["timestamp"]),
            "latitude": float(row["latitude"]),
            "longitude": float(row["longitude"]),
            "rain": float(row["rain"]),
            "traffic_speed": float(
                row["traffic_speed"]
            ),
            "complaints": int(
                row["complaints"]
            ),
            "outage_count": int(
                row["outage_count"]
            ),
            "anomaly_score": float(
                row["anomaly_score"]
            )
        })

    return {
        "count": len(records),
        "anomalies": records
    }