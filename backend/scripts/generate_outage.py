import pandas as pd
import numpy as np

np.random.seed(42)

# Weather data
weather = pd.read_csv("data/weather.csv")

df = pd.DataFrame({
    "timestamp": weather["timestamp"],
    "latitude": weather["latitude"],
    "longitude": weather["longitude"],
})

rain = weather["rain"].fillna(0)

# Normal number of outage incidents
df["outage_count"] = np.random.poisson(1, len(df))

# Rain increases chance of outages
df["outage_count"] += (rain * 2).astype(int)

# Affected customers
df["affected_customers"] = (
    df["outage_count"] * np.random.randint(20, 100, len(df))
)

# Outage duration in minutes
df["outage_duration_min"] = np.random.normal(35, 15, len(df))

# Rain can increase duration
df["outage_duration_min"] += rain * 10

# Keep realistic
df["outage_duration_min"] = df["outage_duration_min"].clip(5, 180)

# Save
df.to_csv("data/power_outages.csv", index=False)

print("Power outage dataset created successfully!")
print(f"Rows: {len(df)}")
print(df.head())