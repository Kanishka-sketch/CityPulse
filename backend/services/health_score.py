import pandas as pd


INPUT_FILE = "data/citypulse_anomalies.csv"


def calculate_health_score():

    df = pd.read_csv(INPUT_FILE)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Latest civic observation
    latest = df.sort_values("timestamp").iloc[-1]

    score = 100

    penalties = {}

    # -----------------------------------
    # 1. Rain penalty
    # -----------------------------------

    rain = float(latest["rain"])

    if rain > 0:
        rain_penalty = min(rain * 4, 15)
    else:
        rain_penalty = 0

    score -= rain_penalty
    penalties["rain"] = round(rain_penalty, 2)

    # -----------------------------------
    # 2. Traffic penalty
    # -----------------------------------

    traffic = float(latest["traffic_speed"])

    if traffic < 45:
        traffic_penalty = min((45 - traffic) * 1.5, 20)
    else:
        traffic_penalty = 0

    score -= traffic_penalty
    penalties["traffic"] = round(traffic_penalty, 2)

    # -----------------------------------
    # 3. Complaints penalty
    # -----------------------------------

    complaints = float(latest["complaints"])

    if complaints > 12:
        complaint_penalty = min(
            (complaints - 12) * 1.2,
            15
        )
    else:
        complaint_penalty = 0

    score -= complaint_penalty
    penalties["complaints"] = round(
        complaint_penalty,
        2
    )

    # -----------------------------------
    # 4. Air quality penalty
    # -----------------------------------

    pm25 = float(latest["pm25"])

    if pm25 > 35:
        air_penalty = min(
            (pm25 - 35) * 0.5,
            20
        )
    else:
        air_penalty = 0

    score -= air_penalty
    penalties["air_quality"] = round(
        air_penalty,
        2
    )

    # -----------------------------------
    # 5. Power outage penalty
    # -----------------------------------

    outages = float(latest["outage_count"])

    if outages > 0:
        outage_penalty = min(
            outages * 5,
            20
        )
    else:
        outage_penalty = 0

    score -= outage_penalty
    penalties["power_outage"] = round(
        outage_penalty,
        2
    )

    # -----------------------------------
    # 6. ML anomaly penalty
    # -----------------------------------

    is_anomaly = bool(latest["is_anomaly"])

    if is_anomaly:
        anomaly_penalty = 15
    else:
        anomaly_penalty = 0

    score -= anomaly_penalty

    penalties["anomaly"] = anomaly_penalty

    # -----------------------------------
    # Keep score between 0 and 100
    # -----------------------------------

    score = max(0, min(100, score))

    score = round(score, 1)

    # -----------------------------------
    # Status
    # -----------------------------------

    if score >= 80:
        status = "Healthy"

    elif score >= 60:
        status = "Watch"

    else:
        status = "Critical"

    return {
        "timestamp": str(latest["timestamp"]),
        "health_score": score,
        "status": status,
        "penalties": penalties,
        "location": {
            "latitude": float(
                latest["latitude"]
            ),
            "longitude": float(
                latest["longitude"]
            )
        }
    }


# -----------------------------------
# Test
# -----------------------------------

if __name__ == "__main__":

    result = calculate_health_score()

    print("\n================================")
    print("CITYPULSE HEALTH SCORE")
    print("================================")

    print(
        f"\nHealth Score: "
        f"{result['health_score']}/100"
    )

    print(
        f"Status: {result['status']}"
    )

    print("\nPenalty Breakdown:")

    for key, value in result[
        "penalties"
    ].items():

        print(
            f"  • {key}: -{value}"
        )

    print("\n================================")