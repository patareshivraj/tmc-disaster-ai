# Universal Prediction Engine Architecture

## 1. Overview
The **Universal Prediction Engine** (and its companion, the **Fire Prediction Engine**) is a newly integrated AI module designed to transform the TMC Disaster Management AI Platform from a Flood-specific tool into a comprehensive **12-Disaster Command Engine**.

This architecture completely eliminates static category arrays and instead dynamically interfaces with the live `tmc2` MySQL database to discover, baseline, and calculate risks for any disaster registered in the system.

## 2. Core Philosophy: Active vs. Baseline Threats
The system distinguishes between two classes of disasters to prevent alert fatigue:
1. **Active Weather Threats (e.g., Heat Waves, Floods, Fires):** Probabilities are spiked dynamically by real-time physics and environmental payload data (Temperature, Humidity, Rainfall).
2. **Historical Baseline Risks (e.g., Road Accidents, Chemical Leaks):** Probabilities are calculated purely from historical incident frequencies in the specific Ward.

## 3. Data Flow
1. **API Request:** Frontend submits `POST /api/ai/universal-prediction/` with environmental data (`ward`, `temperature`, `humidity`, `rainfall`, `water_level`, `is_monsoon`).
2. **Discovery Query:** The Engine executes `SELECT name FROM dmd_disaster_category` to discover all supported disasters dynamically.
3. **Historical Frequency Query:** The Engine joins `dmd_incident` and `dmd_ward` to calculate the exact count of historical incidents for each discovered category within the target ward.
4. **Heuristic Engine:** 
   * A logarithmic baseline cap (Max 40% probability) is applied based on history.
   * Physics-driven heuristics add additional risk (e.g., `temp > 40C` triggers +80% Heat Wave risk).
5. **Output Matrix:** The results are sorted and split into `active_weather_threats` and `historical_baseline_risks`.

## 4. Fire Prediction Engine (Standalone)
A standalone `/api/ai/fire-prediction/` endpoint is provided for specific Fire Brigade dashboards. It uses similar environmental heuristics (Temperature, Humidity) and explicitly filters the database for `Fire` and `Electric Hazard` incidents.

## 5. System Contracts
* **Engine File:** `ai_engine/models/universal_model.py`
* **Serializer:** `UniversalPredictionSerializer` (`ai_api/serializers.py`)
* **Service:** `AIServiceLayer.get_universal_prediction()` (`ai_api/services.py`)
* **Endpoint:** `POST /api/ai/universal-prediction/`

## 6. Future Proofing
Because the engine uses `SELECT name FROM dmd_disaster_category`, if the municipality adds new disaster categories in the future, the Universal Prediction Engine will automatically include them in the threat matrix with zero code changes required.
