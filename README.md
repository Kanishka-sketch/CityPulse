# CityPulse — Live Civic Health Dashboard

> A unified civic intelligence dashboard that turns multiple city signals into one simple, understandable view of urban health.

## 🚨 Problem

City information is usually scattered across different systems — weather, traffic, citizen complaints, air quality, and power outages.

This makes it difficult for residents and city teams to quickly understand:

- What is happening right now?
- Where is something unusual happening?
- Which civic signals changed together?
- Why was an area flagged?

## 💡 Our Solution

**CityPulse** combines multiple civic data streams into a single dashboard.

It processes the data, detects unusual patterns using Machine Learning, identifies relationships between signals, and explains the detected situation in plain language.

### Core Flow

**Data Sources → Data Fusion → Normalization → ML Anomaly Detection → Correlation Analysis → Why Engine → Evidence Trail → Interactive Dashboard**

---

## ✨ Key Features

### 1. City Health Score
A simple 0–100 civic health score based on current city conditions.

### 2. Multi-Signal Civic Monitoring
CityPulse monitors:

- 🌧️ Rainfall
- 🚗 Traffic speed
- 📝 Citizen complaints
- 🌫️ PM2.5 air quality
- ⚡ Power outages

### 3. ML-Based Anomaly Detection
We use **Isolation Forest**, an unsupervised Machine Learning algorithm, to identify unusual combinations of civic conditions.

### 4. Correlation Analysis
CityPulse calculates historical relationships between signals such as:

- Rainfall ↔ Citizen complaints
- Rainfall ↔ Traffic
- Rainfall ↔ Power outages
- Air quality ↔ Traffic

> Correlation is presented as an observed relationship and does not imply causation.

### 5. Why Engine
Instead of simply showing an alert, CityPulse explains what the citizen should know.

Example:

> "Multiple civic signals changed together."

The system identifies contributing signals and presents them in plain language.

### 6. Evidence Trail
Clicking an anomaly on the map reveals the evidence behind the detection:

- Traffic speed
- Rainfall
- Citizen complaints
- PM2.5
- Power outages
- Isolation Forest anomaly signal
- Historical relationships

This makes the anomaly detection more transparent and explainable.

### 7. Interactive City Map
The dashboard visualizes unusual activity across multiple Jaipur monitoring zones using Leaflet.

### 8. Recent Anomaly Activity
Users can see recently detected unusual civic patterns with their timestamp and location.

---

## 🧠 Technology Stack

### Frontend
- React
- Vite
- JavaScript
- CSS
- Leaflet / React Leaflet
- Recharts

### Backend
- Python
- FastAPI
- Pandas
- NumPy

### Machine Learning
- Scikit-learn
- Isolation Forest

### Data Processing
- CSV-based civic datasets
- Data cleaning
- Normalization
- Data fusion
- Rolling correlation analysis

### Development
- Git
- GitHub
- VS Code

---

## 🏗️ Architecture

```text
                 CITYPULSE
                     |
        ┌────────────┴────────────┐
        │                         │
   Civic Data Sources        React Frontend
        │                         │
        │                         │
        └──────────┬──────────────┘
                   ↓
             FastAPI Backend
                   ↓
             Data Processing
                 Pandas
                   ↓
              Normalization
                   ↓
        ┌──────────┼──────────┐
        ↓          ↓          ↓
     Anomaly   Correlation  Health
    Detection   Analysis     Score
   Isolation
     Forest
        │          │          │
        └──────────┼──────────┘
                   ↓
               Why Engine
                   ↓
             Evidence Trail
                   ↓
          React + Interactive Map
