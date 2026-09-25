import pandas as pd
import os

INPUT_FILE = "data/citypulse_fused.csv"
OUTPUT_FILE = "data/citypulse_clean.csv"

# Load fused dataset
df = pd.read_csv(INPUT_FILE)

print("================================")
print("CITYPULSE DATA QUALITY CHECK")
print("================================")

print("Initial rows:", len(df))

# --------------------------------
# 1. Timestamp cleaning
# --------------------------------

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce"
)

# --------------------------------
# 2. Remove duplicate rows
# --------------------------------

duplicates = df.duplicated().sum()
print("Duplicate rows:", duplicates)

df = df.drop_duplicates()

# --------------------------------
# 3. Missing values
# --------------------------------

missing = df.isna().sum()

print("\nMissing values:")
print(missing[missing > 0])

# Remove rows with missing critical values
critical_columns = [
    "timestamp",
    "latitude",
    "longitude"
]

df = df.dropna(subset=critical_columns)

# --------------------------------
# 4. Numeric conversion
# --------------------------------

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

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

# --------------------------------
# 5. Remove impossible values
# --------------------------------

if "traffic_speed" in df.columns:
    df = df[df["traffic_speed"] >= 0]

if "pm25" in df.columns:
    df = df[df["pm25"] >= 0]

if "pm10" in df.columns:
    df = df[df["pm10"] >= 0]

if "complaints" in df.columns:
    df = df[df["complaints"] >= 0]

if "outage_count" in df.columns:
    df = df[df["outage_count"] >= 0]

if "affected_customers" in df.columns:
    df = df[df["affected_customers"] >= 0]

if "outage_duration_min" in df.columns:
    df = df[df["outage_duration_min"] >= 0]

# --------------------------------
# 6. Sort by timestamp
# --------------------------------

df = df.sort_values("timestamp")

# --------------------------------
# 7. Save cleaned dataset
# --------------------------------

df.to_csv(OUTPUT_FILE, index=False)

print("\n================================")
print("CLEANING COMPLETE")
print("================================")
print("Final rows:", len(df))
print("Final columns:", len(df.columns))
print("Saved to:", OUTPUT_FILE)