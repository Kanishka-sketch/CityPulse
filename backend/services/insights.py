import pandas as pd


# -----------------------------------
# Files
# -----------------------------------

ANOMALY_FILE = "data/citypulse_anomalies.csv"
CORRELATION_FILE = "data/citypulse_correlations.csv"


# -----------------------------------
# Thresholds
# -----------------------------------

RAIN_THRESHOLD = 1.0
TRAFFIC_LOW_THRESHOLD = 35
COMPLAINT_THRESHOLD = 18
PM25_HIGH_THRESHOLD = 60
OUTAGE_THRESHOLD = 3


# -----------------------------------
# Historical correlation threshold
# -----------------------------------

MEANINGFUL_CORRELATION = 0.20


# -----------------------------------
# Why Engine
# -----------------------------------

def generate_insight():

    # Load data
    anomalies = pd.read_csv(ANOMALY_FILE)
    correlations = pd.read_csv(CORRELATION_FILE)

    # Prepare timestamp
    anomalies["timestamp"] = pd.to_datetime(
        anomalies["timestamp"]
    )

    anomalies = anomalies.sort_values(
        "timestamp"
    ).reset_index(drop=True)

    # -----------------------------------
    # Latest observation
    # -----------------------------------

    latest = anomalies.iloc[-1]

    reasons = []

    # -----------------------------------
    # Detect unusual current conditions
    # -----------------------------------

    if latest["rain"] >= RAIN_THRESHOLD:
        reasons.append(
            "Rainfall is elevated"
        )

    if latest["traffic_speed"] <= TRAFFIC_LOW_THRESHOLD:
        reasons.append(
            "Traffic speed is below normal"
        )

    if latest["complaints"] >= COMPLAINT_THRESHOLD:
        reasons.append(
            "Citizen complaints are elevated"
        )

    if latest["pm25"] >= PM25_HIGH_THRESHOLD:
        reasons.append(
            "PM2.5 level is elevated"
        )

    if latest["outage_count"] >= OUTAGE_THRESHOLD:
        reasons.append(
            "Multiple power outages are reported"
        )

    # -----------------------------------
    # Current anomaly
    # -----------------------------------

    is_anomaly = bool(latest["is_anomaly"])

    # -----------------------------------
    # Valid correlations
    # -----------------------------------

    valid_correlations = correlations[
        correlations["status"] == "valid"
    ].copy()

    # Convert correlation to numeric
    if not valid_correlations.empty:

        valid_correlations["correlation"] = pd.to_numeric(
            valid_correlations["correlation"],
            errors="coerce"
        )

    # Meaningful relationships
    meaningful = valid_correlations[
        valid_correlations["correlation"].abs()
        >= MEANINGFUL_CORRELATION
    ].copy()

    evidence = []

    for _, row in meaningful.iterrows():

        correlation = float(row["correlation"])

        evidence.append({
            "signal_1": row["signal_1"],
            "signal_2": row["signal_2"],
            "correlation": correlation,
            "strength": row["strength"],
            "direction": row["direction"],
            "message": (
                f"{row['signal_1']} and "
                f"{row['signal_2']} show a "
                f"{row['strength']} "
                f"{row['direction']} relationship "
                f"(correlation {correlation:.2f})"
            )
        })

    # -----------------------------------
    # If current rolling correlations
    # are weak, use historical evidence
    # from the same dataset.
    # -----------------------------------

    historical_evidence = []

    if not evidence:

        numeric_columns = [
            "rain",
            "pm25",
            "traffic_speed",
            "complaints",
            "outage_count",
            "affected_customers"
        ]

        historical_matrix = anomalies[
            numeric_columns
        ].corr()

        for signal_a, signal_b in [
            ("rain", "traffic_speed"),
            ("rain", "complaints"),
            ("rain", "outage_count"),
            ("rain", "affected_customers"),
            ("traffic_speed", "complaints"),
            ("pm25", "traffic_speed")
        ]:

            value = historical_matrix.loc[
                signal_a,
                signal_b
            ]

            if pd.isna(value):
                continue

            if abs(value) < MEANINGFUL_CORRELATION:
                continue

            if value > 0:
                direction = "positive"
            else:
                direction = "negative"

            abs_value = abs(value)

            if abs_value >= 0.7:
                strength = "strong"
            elif abs_value >= 0.4:
                strength = "moderate"
            else:
                strength = "weak"

            historical_evidence.append({
                "signal_1": signal_a,
                "signal_2": signal_b,
                "correlation": round(float(value), 3),
                "strength": strength,
                "direction": direction,
                "message": (
                    f"{signal_a} and {signal_b} show a "
                    f"{strength} {direction} historical "
                    f"relationship "
                    f"(correlation {value:.2f})"
                )
            })

    # -----------------------------------
    # Combine evidence
    # -----------------------------------

    all_evidence = evidence + historical_evidence

    # -----------------------------------
    # Overall status
    # -----------------------------------

    if is_anomaly and len(reasons) >= 2:

        status = "warning"

        message = (
            "Possible civic disruption detected"
        )

    elif is_anomaly or len(reasons) >= 1:

        status = "watch"

        message = (
            "Unusual civic conditions detected"
        )

    else:

        status = "normal"

        message = (
            "Civic conditions appear normal"
        )

    # -----------------------------------
    # Final result
    # -----------------------------------

    insight = {

        "timestamp": str(
            latest["timestamp"]
        ),

        "status": status,

        "message": message,

        "anomaly_detected": is_anomaly,

        "reasons": reasons,

        "correlations": all_evidence,

        "location": {
            "latitude": float(
                latest["latitude"]
            ),
            "longitude": float(
                latest["longitude"]
            )
        },

        "current_metrics": {
            "rain": float(
                latest["rain"]
            ),
            "pm25": float(
                latest["pm25"]
            ),
            "traffic_speed": float(
                latest["traffic_speed"]
            ),
            "complaints": int(
                latest["complaints"]
            ),
            "outage_count": int(
                latest["outage_count"]
            )
        }
    }

    return insight


# -----------------------------------
# Test
# -----------------------------------

if __name__ == "__main__":

    result = generate_insight()

    print("\n================================")
    print("CITYPULSE WHY ENGINE")
    print("================================")

    print(
        f"\nStatus: {result['status']}"
    )

    print(
        f"Message: {result['message']}"
    )

    print("\nReasons:")

    if result["reasons"]:

        for reason in result["reasons"]:
            print(f"  • {reason}")

    else:

        print(
            "  • No unusual conditions detected"
        )

    print("\nSupporting Relationships:")

    if result["correlations"]:

        for item in result["correlations"]:

            print(
                f"  • {item['signal_1']} ↔ "
                f"{item['signal_2']} : "
                f"{item['correlation']} "
                f"({item['strength']}, "
                f"{item['direction']})"
            )

    else:

        print(
            "  • No meaningful relationship available"
        )

    print("\nCurrent Metrics:")

    for key, value in result[
        "current_metrics"
    ].items():

        print(
            f"  • {key}: {value}"
        )

    print("\n================================")