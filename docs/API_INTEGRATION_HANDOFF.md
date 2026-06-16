# TMC Disaster Management AI: API Integration Handoff

**Target Audience:** Frontend Teams (React, Next.js, Mobile) & Backend Teams (Django, Node.js, API Gateway).  
**Purpose:** This document is the single source of truth for interacting with the completely decoupled AI Intelligence Layer. 

---

## 1. Architectural Overview

The AI Platform is designed as a **Headless Intelligence Microservice**. 

* **The AI Layer DOES:** Connect to the `tmc2` MySQL database via a read-only adapter, run complex machine learning, extract actuarial statistics, and return structured JSON risk analyses.
* **The AI Layer DOES NOT:** Handle authentication, process user logins, create new database rows, or render UI dashboards.

### ⚙️ Backend Team Responsibilities
1. **Perimeter Security:** You must wrap the `/api/ai/` routes behind your API Gateway or Django Authentication logic (JWT, Session). The AI endpoints currently have `AllowAny` permissions for internal decoupling.
2. **Data Ingestion:** The AI reads from tables like `dmd_weather_history` and `dmd_building`. The Backend team must build the standard CRUD APIs that insert new rows into these tables.
3. **Database Schema:** If you alter the database schema (e.g., renaming `dmd_ward.name` to `dmd_ward.title`), you must inform the AI team, as the AI Repository layer maps explicitly to the current 3NF schema.

### 💻 Frontend Team Responsibilities
1. **Asynchronous Handling:** AI processing is mathematically heavy. Always implement loading spinners while awaiting API responses.
2. **Explainable UI:** The JSON outputs contain arrays like `learned_risk_factors` and `recommendations`. Do not just show the raw `risk_score`. Build UIs that display *why* the AI made the decision using these string arrays.
3. **No Direct DB Calls:** You only need to consume these REST APIs. Do not query the AI database yourself.

---

## 2. Global Request & Response Format

**Base URL:** `http://<your-server-ip>/api/ai/`
**Content-Type:** `application/json`

### Error Handling
If an invalid payload is sent, the API returns `HTTP 400 Bad Request` with strict field-level errors:
```json
{
    "temperature": ["This field is required."]
}
```

If an ID is missing from the live database, the API returns `HTTP 404 Not Found`.

---

## 3. The Endpoints (API Contracts)

### A. Flood Prediction AI
Predicts the exact probability of a flood based on current weather patterns and soil saturation baselines.

* **Method:** `POST`
* **Endpoint:** `/flood-prediction/`
* **Request Body:**
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
* **Response Body (200 OK):**
```json
{
    "ward": "Diva",
    "flood_probability": 43.43,
    "risk_level": "High",
    "confidence": 56.57
}
```

---

### B. Ward Risk AI
Calculates the overarching geographical and statistical vulnerability of a specific ward.

* **Method:** `GET`
* **Endpoint:** `/ward-risk/<str:ward_name>/`
* **Example:** `/ward-risk/Diva/`
* **Request Body:** *None*
* **Response Body (200 OK):**
```json
{
    "ward": "Diva",
    "risk_score": 68.32,
    "risk_level": "High Risk",
    "risk_factors": [
        "Base Geographic Exposure",
        "Low Preparedness Score"
    ],
    "recommendations": [
        "Increase Weather Monitoring",
        "Deploy Additional Pumps"
    ]
}
```

---

### C. Resource Recommendation AI
Determines exactly how much physical equipment is missing for an ongoing incident.

* **Method:** `POST`
* **Endpoint:** `/resource-recommendation/`
* **Request Body:**
```json
{
    "ward": "Diva",
    "flood_probability": 43.43,
    "risk_score": 68.32,
    "risk_factors": []
}
```
* **Response Body (200 OK):**
```json
{
    "ward": "Diva",
    "priority_rank": 1,
    "resource_demand_score": 66.49,
    "resource_gap_score": 100.0,
    "resource_shortage_score": 65.0,
    "resources_needed": [
        {
            "resource": "Water Pumps",
            "required": 3,
            "available": 0,
            "shortage": 3,
            "reason": "Data-driven requirement (3) exceeds current inventory (0)."
        }
    ],
    "recommendations": ["Deploy Additional Pumps"]
}
```

---

### D. Building Advisor AI
Calculates the actuarial probability of building collapse based on age, condition, and delays in structural auditing.

* **Method:** `POST`
* **Endpoint:** `/building-advisor/`
* **Request Body:**
```json
{
    "building_id": "1" 
}
```
*(Note: Send the integer ID as a string)*
* **Response Body (200 OK):**
```json
{
    "building_id": "1",
    "building_name": "Sai Darshan",
    "ward": "Diva",
    "risk_score": 93.0,
    "collapse_probability": 58.65,
    "classification": "Evacuation / Demolition Candidate",
    "learned_risk_factors": [
        {
            "factor": "Age 41-60 Years",
            "historical_high_risk_rate": 51.3
        }
    ],
    "recommendations": [
        "Immediate Evacuation",
        "Demolition Assessment"
    ],
    "confidence": 67.4
}
```

---

### E. Incident Forecast AI
Projects short-term incident volumes based on historical seasonal velocity. Highly recommended for Dashboard "Home Pages".

* **Method:** `POST`
* **Endpoint:** `/forecast/`
* **Request Body:**
```json
{
    "days": 7
}
```
* **Response Body (200 OK):**
```json
{
    "forecast_period": "7_days",
    "expected_incidents": 10,
    "hotspots": ["Mumbra", "Kalwa", "Diva"],
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

### F. Apex Recommendation Engine
Fuses all distinct AI components into a final, executive-level decision. 

* **Method:** `POST`
* **Endpoint:** `/recommendations/`
* **Request Body:**
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
* **Response Body (200 OK):**
```json
{
    "ward": "Diva",
    "final_priority_score": 77.29,
    "escalation_level": "Level 4 (Critical Emergency)",
    "actionable_directives": [
        "Declare Ward-level Emergency",
        "Mobilize All Available Resources",
        "Coordinate with State Disaster Forces (SDRF)"
    ]
}
```

---

### G. Natural Language Chatbot
A single endpoint capable of parsing typed questions and invoking the other APIs automatically. Best used for Search Bars and Assistant UIs.

* **Method:** `POST`
* **Endpoint:** `/chatbot/`
* **Request Body:**
```json
{
    "question": "What is the building risk for building ID 1?"
}
```
* **Response Body (200 OK):**
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
    "modules_used": ["Building Advisor"],
    "confidence": 98.5
}
```
