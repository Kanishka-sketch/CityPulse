import pandas as pd
import numpy as np

rng = np.random.default_rng(101)

# Same 360 hourly timestamps as weather data
weather = pd.read_csv("data/weather.csv")
df = pd.DataFrame({
    "timestamp": weather["timestamp"],
    "latitude": weather["latitude"],
    "longitude": weather["longitude"],
})

# Base PM2.5
df["pm25"] = rng.normal(55, 12, len(df))

# Rain-related variation
rain = weather["rain"].fillna(0)

# Keep PM2.5 realistic and non-negative
df["pm25"] = df["pm25"] - (rain * 8)
df["pm25"] = df["pm25"].clip(lower=10)

# PM10 approximately correlated with PM2.5
df["pm10"] = df["pm25"] * rng.uniform(1.5, 2.0, len(df))
# Other pollutants
df["no2"] = rng.normal(30, 8, len(df)).clip(5)
df["o3"] = rng.normal(40, 10, len(df)).clip(5)

df.to_csv("data/air_quality.csv", index=False)

print("Air quality dataset created successfully!")
print(f"Rows: {len(df)}")
print(df.head())