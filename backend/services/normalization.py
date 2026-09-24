import pandas as pd

INPUT_FILE = "data/citypulse_clean.csv"
OUTPUT_FILE = "data/citypulse_normalized.csv"


def normalize_data():

    # Load cleaned data
    df = pd.read_csv(INPUT_FILE)

    # -----------------------------
    # 1. Normalize timestamp
    # -----------------------------
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

    # -----------------------------
    # 2. Normalize location
    # -----------------------------
    df["latitude"] = pd.to_numeric(
        df["latitude"],
        errors="coerce"
    )

    df["longitude"] = pd.to_numeric(
        df["longitude"],
        errors="coerce"
    )

    # -----------------------------
    # 3. Normalize numeric columns
    # -----------------------------
    numeric_columns = [
        "temperature",
        "humidity",
        "precipitation",
        "rain",
        "wind_speed",
        "pm25",
        "pm10",
        "no2",
        "o3",
        "traffic_speed",
        "complaints",
        "outage_count",
        "affected_customers",
        "outage_duration_min"
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # -----------------------------
    # 4. Remove invalid rows
    # -----------------------------
    df = df.dropna(
        subset=["timestamp", "latitude", "longitude"]
    )

    # -----------------------------
    # 5. Sort by timestamp
    # -----------------------------
    df = df.sort_values("timestamp")

    # -----------------------------
    # 6. Save normalized data
    # -----------------------------
    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("================================")
    print("NORMALIZATION COMPLETE")
    print("================================")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print("Timestamp:", df["timestamp"].dtype)
    print("Latitude:", df["latitude"].dtype)
    print("Longitude:", df["longitude"].dtype)
    print()
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    normalize_data()