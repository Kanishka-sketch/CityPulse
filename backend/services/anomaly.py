import pandas as pd
import joblib
import os

from sklearn.ensemble import IsolationForest


INPUT_FILE = "data/citypulse_normalized.csv"
OUTPUT_FILE = "data/citypulse_anomalies.csv"
MODEL_FILE = "models/anomaly_model.pkl"


# ==========================================
# 1. LOAD DATA
# ==========================================

df = pd.read_csv(INPUT_FILE)

print("Data loaded:", len(df), "rows")


# ==========================================
# 2. SELECT FEATURES
# ==========================================

features = [
    "rain",
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

X = df[features].copy()

# Handle any missing values
X = X.fillna(X.median())


# ==========================================
# 3. TRAIN ISOLATION FOREST
# ==========================================

model = IsolationForest(
    n_estimators=150,
    contamination=0.08,
    random_state=42
)

model.fit(X)


# ==========================================
# 4. DETECT ANOMALIES
# ==========================================

df["anomaly_prediction"] = model.predict(X)

df["anomaly_score"] = model.decision_function(X)

df["is_anomaly"] = (
    df["anomaly_prediction"] == -1
)


# ==========================================
# 5. SAVE MODEL
# ==========================================

os.makedirs("models", exist_ok=True)

joblib.dump(
    {
        "model": model,
        "features": features
    },
    MODEL_FILE
)


# ==========================================
# 6. SAVE RESULTS
# ==========================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ==========================================
# 7. DISPLAY RESULTS
# ==========================================

anomaly_count = df["is_anomaly"].sum()

print("\n================================")
print("ML ANOMALY DETECTION COMPLETE")
print("================================")

print("Total observations :", len(df))
print("Anomalies detected  :", anomaly_count)
print("Normal observations :", len(df) - anomaly_count)

print("\nModel: Isolation Forest")
print("Features used:", len(features))

print("\nModel saved to:")
print(MODEL_FILE)

print("\nResults saved to:")
print(OUTPUT_FILE)

print("\nTop anomalies:")

print(
    df[df["is_anomaly"]][
        [
            "timestamp",
            "rain",
            "pm25",
            "traffic_speed",
            "complaints",
            "outage_count",
            "anomaly_score"
        ]
    ]
    .sort_values("anomaly_score")
    .head(10)
)