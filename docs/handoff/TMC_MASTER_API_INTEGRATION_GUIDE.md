# TMC MASTER API INTEGRATION GUIDE
**The Ultimate Single-File Reference for Frontend & Backend Teams**

This document contains **everything** required to fully integrate the TMC Disaster Management AI Layer into any Dashboard (Frontend) or Gateway (Backend). It includes every endpoint, every payload, and exact data types.

**Base API URL:** `http://localhost:8000/api/ai`
**Authentication:** Currently `AllowAny` (Needs JWT Implementation by Backend Team)
**Format:** `application/json`

---

## 1. UNIVERSAL PREDICTION API
**Purpose:** Predict 360-degree risk matrix across 12 disaster categories.
*   **Method:** `POST`
*   **Endpoint:** `/api/ai/universal-prediction/`

### Input Payload (Frontend Sends)
```json
{
  "ward": "Mumbra",
  "temperature": 41.5,
  "humidity": 12.0,
  "rainfall": 0.0,
  "water_level": 0.0,
  "is_monsoon": 0
}
```
*   `ward` (String): Ward name.
*   `temperature` (Float): Current temp in Celsius.
*   `humidity` (Float): Humidity percentage (0-100).
*   `rainfall` (Float): Rainfall in mm.
*   `water_level` (Float): River/lake water level in meters.
*   `is_monsoon` (Integer): 1 if monsoon season, 0 if not.

### Output Payload (Backend/AI Returns)
```json
{
  "ward": "Mumbra",
  "timestamp": "2026-06-18T13:56:37",
  "active_weather_threats": [
    {
      "disaster": "Heat Wave",
      "probability": 86.64,
      "severity_level": "Critical",
      "historical_count_in_ward": 83
    }
  ],
  "historical_baseline_risks": [
    {
      "disaster": "Road Accident",
      "probability": 14.32,
      "severity_level": "Low",
      "historical_count_in_ward": 179
    }
  ]
}
```

---

## 2. FLOOD PREDICTION API
**Purpose:** Predict localized flood probability.
*   **Method:** `POST`
*   **Endpoint:** `/api/ai/flood-prediction/`

### Input Payload (Frontend Sends)
```json
{
  "ward": "Diva",
  "rainfall": 150.0,
  "humidity": 85.0,
  "water_level": 2.5,
  "temperature": 30.0,
  "previous_flood_count": 0,
  "is_monsoon": 1
}
```
*   `ward` (String): Ward name.
*   `rainfall` (Float): Rainfall in mm.
*   `humidity` (Float): Humidity percentage (0-100).
*   `water_level` (Float): River/lake water level in meters.
*   `temperature` (Float): Current temp in Celsius.
*   `previous_flood_count` (Integer): Number of times flooded this year.
*   `is_monsoon` (Integer): 1 if monsoon season, 0 if not.

### Output Payload (Backend/AI Returns)
```json
{
  "ward": "Diva",
  "flood_probability": 43.43,
  "risk_level": "High",
  "confidence": 56.57
}
```

---

---

## 3. FIRE PREDICTION API
**Purpose:** Predict fire and electrical hazard probability.
*   **Method:** `POST`
*   **Endpoint:** `/api/ai/fire-prediction/`

### Input Payload (Frontend Sends)
```json
{
  "ward": "Mumbra",
  "temperature": 41.5,
  "humidity": 12.0
}
```
*   `ward` (String): Ward name.
*   `temperature` (Float): Current temp in Celsius.
*   `humidity` (Float): Humidity percentage (0-100).

### Output Payload (Backend/AI Returns)
```json
{
  "ward": "Mumbra",
  "fire_probability": 85.5,
  "risk_level": "Critical",
  "confidence": 95.0
}
```

---

## 4. WARD RISK API
**Purpose:** Fetch total aggregated disaster risk for a single ward.
*   **Method:** `GET`
*   **Endpoint:** `/api/ai/ward-risk/<str:ward>/`
*   *Example URL:* `/api/ai/ward-risk/Diva/`

### Input Payload
*(No JSON Body required. Pass the ward name in the URL path.)*

### Output Payload (Backend/AI Returns)
```json
{
  "ward": "Diva",
  "risk_score": 68.32,
  "risk_level": "High",
  "confidence": 88.5,
  "risk_factors": [
    "Frequent Flooding",
    "High Building Risk"
  ],
  "recommendations": [
    "Deploy Additional Pumps",
    "Immediate Structural Audit"
  ]
}
```

---

## 3. RESOURCE RECOMMENDATION API
**Purpose:** Predict asset shortages (boats, pumps) based on risk factors.
*   **Method:** `POST`
*   **Endpoint:** `/api/ai/resource-recommendation/`

### Input Payload (Frontend Sends)
```json
{
  "ward": "Diva",
  "flood_probability": 90.0,
  "risk_score": 95.0,
  "risk_factors": []
}
```
*   `ward` (String): Ward name.
*   `flood_probability` (Float): Must be between 0.0 and 100.0.
*   `risk_score` (Float): Must be between 0.0 and 100.0.
*   `risk_factors` (List of Strings): Optional.

### Output Payload (Backend/AI Returns)
```json
{
  "ward": "Diva",
  "resource_demand_score": 88.5,
  "resource_gap_score": 45.2,
  "resources_needed": [
    "5 High-Capacity Pumps",
    "12 Rescue Boats"
  ],
  "priority_rank": 1,
  "confidence": 92.4
}
```

---

## 4. BUILDING ADVISOR API
**Purpose:** Analyze structural collapse risk of older TMC buildings.
*   **Method:** `POST`
*   **Endpoint:** `/api/ai/building-advisor/`

### Input Payload (Frontend Sends)
```json
{
  "building_id": "1"
}
```
*   `building_id` (String): Must match exactly with a building ID in the TMC database.

### Output Payload (Backend/AI Returns)
```json
{
  "building_id": "1",
  "building_name": "Sai Darshan",
  "ward": "Diva",
  "age_years": 45.0,
  "collapse_probability": 58.65,
  "classification": "Evacuation / Demolition Candidate",
  "risk_factors": [
    "Age > 40 Years",
    "Poor Condition"
  ],
  "recommended_actions": [
    "Immediate Evacuation",
    "Demolition Assessment"
  ],
  "confidence": 98.5
}
```

---

## 5. INCIDENT FORECAST API
**Purpose:** Predict emergency volume over the next X days.
*   **Method:** `POST`
*   **Endpoint:** `/api/ai/forecast/`

### Input Payload (Frontend Sends)
```json
{
  "days": 7
}
```
*   `days` (Integer): Forecast period length (Min 1, Max 365).

### Output Payload (Backend/AI Returns)
```json
{
  "forecast_period": "7_days",
  "expected_incidents": 10,
  "hotspots": [
    "Mumbra",
    "Kalwa",
    "Diva"
  ],
  "category_forecast": {
    "Flood": 5,
    "Tree Fall": 3
  },
  "severity_distribution": {
    "Minor": 40.4,
    "Critical": 10.0
  },
  "explanations": [
    "Base historical volume calculated at 0.76 daily incidents."
  ]
}
```

---

## 6. RECOMMENDATION ENGINE API (APEX ENGINE)
**Purpose:** Combine all AI modules into one massive protocol directive.
*   **Method:** `POST`
*   **Endpoint:** `/api/ai/recommendations/`

### Input Payload (Frontend Sends)
```json
{
  "ward": "Diva",
  "flood_probability": 43.43,
  "ward_risk_score": 68.32,
  "resource_shortage_score": 65.0,
  "building_risk_score": 93.0,
  "forecast_incidents": 10.0,
  "forecast_severity_critical_pct": 10.0
}
```

### Output Payload (Backend/AI Returns)
```json
{
  "ward": "Diva",
  "combined_risk_score": 77.29,
  "priority_level": "Level 4",
  "escalation_level": "Critical Emergency",
  "recommendations": [
    "Declare Ward-level Emergency",
    "Mobilize All Available Resources",
    "Coordinate with State Disaster Forces (SDRF)"
  ],
  "confidence": 88.0
}
```

---

## 9. GENERATIVE COPILOT API
**Purpose:** Provide conversational Agent access to all AI intelligence via Google Gemini.
*   **Method:** `POST`
*   **Endpoint:** `/api/ai/copilot/`

### Input Payload (Frontend Sends)
```json
{
  "question": "What is the building risk for building ID 1?"
}
```
*   `question` (String): Natural language question.

### Output Payload (Backend/AI Returns)
```json
{
  "question": "What is the building risk for building ID 1?",
  "answer": "Building 1 (Sai Darshan) in Diva is currently rated as Evacuation / Demolition Candidate with a collapse probability of 58.65%.",
  "reasoning": [
    "Age 41-60 Years (Risk: 51.3%)"
  ],
  "recommended_actions": [
    "Immediate Evacuation",
    "Demolition Assessment"
  ],
  "modules_used": [
    "Building Advisor"
  ],
  "confidence": 98.5,
  "intent": "BuildingRisk"
}
```

---

## ERROR HANDLING (Universal)

If the Frontend sends invalid data types (e.g., passing a string for `rainfall`), the Backend will return a **400 Bad Request** mapping to the exact fields:

```json
{
  "rainfall": [
    "A valid number is required."
  ],
  "is_monsoon": [
    "Ensure this value is less than or equal to 1."
  ]
}
```

If the AI Model files are missing or offline, the Backend will return a **503 Service Unavailable**:

```json
{
  "status": "error",
  "message": "AI model unavailable"
}
```
