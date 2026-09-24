import pandas as pd
import numpy as np


# -----------------------------
# Configuration
# -----------------------------

INPUT_FILE = "data/citypulse_anomalies.csv"
OUTPUT_FILE = "data/citypulse_correlations.csv"

WINDOW = 24
MIN_PERIODS = 12

SIGNAL_PAIRS = [
    ("rain", "traffic_speed"),
    ("rain", "complaints"),
    ("rain", "outage_count"),
    ("rain", "affected_customers"),
    ("traffic_speed", "complaints"),
    ("pm25", "traffic_speed"),
]


# -----------------------------
# Helper: correlation strength
# -----------------------------

def get_strength(correlation):
    abs_corr = abs(correlation)

    if abs_corr >= 0.7:
        return "strong"
    elif abs_corr >= 0.4:
        return "moderate"
    elif abs_corr >= 0.2:
        return "weak"
    else:
        return "very_weak"


# -----------------------------
# Rolling correlation engine
# -----------------------------

def find_latest_valid_correlation(df, signal_a, signal_b):
    """
    Calculate rolling 24-hour correlation.

    We check ALL windows and keep the most recent
    valid correlation.

    Invalid windows:
    - NaN correlation
    - insufficient observations
    - constant signal
    """

    a = pd.to_numeric(df[signal_a], errors="coerce")
    b = pd.to_numeric(df[signal_b], errors="coerce")

    # Rolling Pearson correlation
    rolling_corr = a.rolling(
        WINDOW,
        min_periods=MIN_PERIODS
    ).corr(b)

    # Check windows from newest -> oldest
    for i in range(len(df) - 1, -1, -1):

        correlation = rolling_corr.iloc[i]

        # Skip NaN / invalid correlations
        if pd.isna(correlation):
            continue

        # Extract the actual window
        start = max(0, i - WINDOW + 1)

        window_a = a.iloc[start:i + 1]
        window_b = b.iloc[start:i + 1]

        # Remove missing values pairwise
        valid = pd.concat(
            [window_a, window_b],
            axis=1
        ).dropna()

        # Need enough observations
        if len(valid) < MIN_PERIODS:
            continue

        # Ignore constant windows
        if valid[signal_a].nunique() <= 1:
            continue

        if valid[signal_b].nunique() <= 1:
            continue

        return {
            "correlation": round(float(correlation), 3),
            "timestamp": df["timestamp"].iloc[i],
            "status": "valid"
        }

    # No valid window found
    return {
        "correlation": None,
        "timestamp": None,
        "status": "insufficient_variation"
    }


# -----------------------------
# Main
# -----------------------------

def main():

    print("\nROLLING CORRELATION ENGINE")
    print(f"Window: Last {WINDOW} hours")
    print("-" * 60)

    # Load normalized/anomaly data
    df = pd.read_csv(INPUT_FILE)

    # Timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Sort chronologically
    df = df.sort_values("timestamp").reset_index(drop=True)

    results = []

    for signal_a, signal_b in SIGNAL_PAIRS:

        result = find_latest_valid_correlation(
            df,
            signal_a,
            signal_b
        )

        if result["status"] == "valid":

            correlation = result["correlation"]

            direction = (
                "positive"
                if correlation > 0
                else "negative"
                if correlation < 0
                else "neutral"
            )

            strength = get_strength(correlation)

            results.append({
                "signal_1": signal_a,
                "signal_2": signal_b,
                "window_hours": WINDOW,
                "correlation": correlation,
                "strength": strength,
                "direction": direction,
                "status": "valid",
                "window_end": result["timestamp"]
            })

            print(
                f"{signal_a:20} ↔ {signal_b:20} "
                f"{correlation:7.3f} "
                f"{strength:10} "
                f"{direction}"
            )

        else:

            results.append({
                "signal_1": signal_a,
                "signal_2": signal_b,
                "window_hours": WINDOW,
                "correlation": None,
                "strength": None,
                "direction": None,
                "status": "insufficient_variation",
                "window_end": None
            })

            print(
                f"{signal_a:20} ↔ {signal_b:20} "
                f"INSUFFICIENT_VARIATION"
            )

    # Save results
    result_df = pd.DataFrame(results)

    result_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n" + "-" * 60)
    print(f"Valid relationships: {(result_df['status'] == 'valid').sum()}")
    print(
        f"Unavailable relationships: "
        f"{(result_df['status'] == 'insufficient_variation').sum()}"
    )
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()