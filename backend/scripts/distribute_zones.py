from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"

# 5 Jaipur monitoring zones
ZONES = [
    (26.9124, 75.7873),  # Central
    (26.9450, 75.7800),  # North
    (26.8750, 75.7900),  # South
    (26.9200, 75.8350),  # East
    (26.9000, 75.7400),  # West
]

FILES = [
    "weather.csv",
    "air_quality.csv",
    "traffic_complaints.csv",
    "power_outages.csv",
]

for filename in FILES:
    path = DATA / filename

    df = pd.read_csv(path)

    if len(df) == 0:
        print(f"Skipping empty file: {filename}")
        continue

    # Same timestamp must receive the same zone
    df["zone_id"] = (
        df.groupby("timestamp").ngroup() % len(ZONES)
    )

    df["latitude"] = df["zone_id"].map(
        lambda z: ZONES[int(z)][0]
    )

    df["longitude"] = df["zone_id"].map(
        lambda z: ZONES[int(z)][1]
    )

    df.drop(columns=["zone_id"], inplace=True)

    df.to_csv(path, index=False)

    print(f"Updated: {filename}")

print("\n5 Jaipur monitoring zones assigned successfully.")