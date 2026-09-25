import requests
import pandas as pd

# Jaipur coordinates
LATITUDE = 26.9124
LONGITUDE = 75.7873

# Development dataset: 15 days
START_DATE = "2026-09-09"
END_DATE = "2026-09-23"

url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "start_date": START_DATE,
    "end_date": END_DATE,
    "hourly": (
        "temperature_2m,"
        "relative_humidity_2m,"
        "precipitation,"
        "rain,"
        "wind_speed_10m,"
        "weather_code"
    ),
    "timezone": "Asia/Kolkata"
}

response = requests.get(url, params=params)

if response.status_code != 200:
    print("API request failed")
    print(response.text)
    exit()

data = response.json()

# Extract hourly data
hourly = data["hourly"]

# Convert JSON → DataFrame
df = pd.DataFrame(hourly)

# Add location
df["latitude"] = data["latitude"]
df["longitude"] = data["longitude"]

# Rename columns
df = df.rename(columns={
    "time": "timestamp",
    "temperature_2m": "temperature",
    "relative_humidity_2m": "humidity",
    "wind_speed_10m": "wind_speed"
})

# Keep required columns
columns = [
    "timestamp",
    "latitude",
    "longitude",
    "temperature",
    "humidity",
    "precipitation",
    "rain",
    "wind_speed",
    "weather_code"
]

df = df[columns]

# Save CSV
output_path = "data/weather.csv"
df.to_csv(output_path, index=False)

print("Weather dataset created successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print("\nFirst 5 rows:")
print(df.head())