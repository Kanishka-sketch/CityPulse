import pandas as pd
import numpy as np

rng = np.random.default_rng(202)

# Weather timestamps use karenge
weather = pd.read_csv("data/weather.csv")

df = pd.DataFrame({
    "timestamp": weather["timestamp"],
    "latitude": weather["latitude"],
    "longitude": weather["longitude"],
})

# -------------------------
# TRAFFIC
# -------------------------

# Normal traffic speed
df["traffic_speed"] = rng.normal(45, 7, len(df))

# Rain -> slower traffic
rain = weather["rain"].fillna(0)
df["traffic_speed"] -= rain * 5

# Keep realistic
df["traffic_speed"] = df["traffic_speed"].clip(10, 65)


# -------------------------
# CIVIC COMPLAINTS
# -------------------------

# Normal complaints per hour
df["complaints"] =rng.poisson(12, len(df))

# Rain -> more complaints
df["complaints"] += (rain * 4).astype(int)

# Keep minimum
df["complaints"] = df["complaints"].clip(lower=0)


# -------------------------
# SAVE
# -------------------------

df.to_csv("data/traffic_complaints.csv", index=False)

print("Traffic + complaints dataset created successfully!")
print(f"Rows: {len(df)}")
print(df.head())