import pandas as pd

# Load all feeds
weather = pd.read_csv("data/weather.csv")
air = pd.read_csv("data/air_quality.csv")
traffic = pd.read_csv("data/traffic_complaints.csv")
outage = pd.read_csv("data/power_outages.csv")

# Merge all feeds
df = weather.merge(
    air,
    on=["timestamp", "latitude", "longitude"],
    how="inner"
)

df = df.merge(
    traffic,
    on=["timestamp", "latitude", "longitude"],
    how="inner"
)

df = df.merge(
    outage,
    on=["timestamp", "latitude", "longitude"],
    how="inner"
)

# Sort chronologically
df = df.sort_values("timestamp")

# Save final fused dataset
df.to_csv("data/citypulse_fused.csv", index=False)

print("================================")
print("CITYPULSE DATA FUSION COMPLETE")
print("================================")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print()
print(df.columns.tolist())
print()
print(df.head())