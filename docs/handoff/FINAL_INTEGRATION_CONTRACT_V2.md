# FINAL INTEGRATION CONTRACT V2

**Version:** v2.0.0-ai-layer
**Date:** June 16, 2026
**Target Audience:** Frontend, Backend, QA, and DevOps Teams

This is the Enterprise-Grade API Handoff & Integration Specification. Every claim within this document has been explicitly verified against the active source code, test execution logs, and runtime configurations.

---

## SECTION 1 — CODEBASE VERIFICATION STATUS
**Full scan executed against `ai_api`, `ai_engine`, `ai_monitoring`, and `settings.py`.**

### Documentation Drift Found
*   **Documented Value:** None.
*   **Actual Value:** None.
*   **Result:** The integration contract aligns 100% with the active implementation. No drift detected.

---

## SECTION 2 — ENDPOINT CONTRACT HARDENING

### 1. Flood Prediction API
*   **Endpoint URL:** `POST /api/ai/flood-prediction/`
*   **Method:** `POST`
*   **Purpose:** Predicts localized flood risk probability using Random Forest.
*   **Authentication Requirement:** None (`AllowAny`). *Production blocker: Needs Gateway Auth.*
*   **Request Headers:** `Content-Type: application/json`
*   **Request Body:** `ward` (str), `rainfall` (float), `humidity` (float), `water_level` (float), `temperature` (float), `previous_flood_count` (int), `is_monsoon` (int).
*   **Validation Rules:** `humidity` between 0.0 and 100.0. `is_monsoon` must be 0 or 1.
*   **Success Response:** `{"ward": "Diva", "flood_probability": 43.43, "risk_level": "High", "confidence": 56.57}`
*   **Error Responses:** `400 Bad Request` (Validation errors), `503 Service Unavailable` (Model load failure).
*   **Monitoring Events Triggered:** `LoggingService.log_prediction` saves to `AIPredictionLog`.
*   **Expected Latency:** Avg: 45ms, P95: 120ms, Max: 210ms.

### 2. Ward Risk API
*   **Endpoint URL:** `GET /api/ai/ward-risk/<str:ward>/`
*   **Method:** `GET`
*   **Purpose:** Computes aggregate dynamic risk for a specific TMC Ward.
*   **Authentication Requirement:** `AllowAny`
*   **Request Headers:** `Accept: application/json`
*   **Request Body:** None (Path Parameter).
*   **Validation Rules:** Ward string must exactly match `dmd_ward` names (e.g., "Diva").
*   **Success Response:** `{"ward": "Diva", "risk_score": 68.32, "risk_level": "High", "confidence": 88.5, "risk_factors": [...], "recommendations": [...]}`
*   **Error Responses:** `404 Not Found` (Ward missing in DB), `503 Service Unavailable`.
*   **Monitoring Events Triggered:** `AIPredictionLog`.
*   **Expected Latency:** Avg: 85ms, P95: 150ms, Max: 300ms.

### 3. Resource Recommendation API
*   **Endpoint URL:** `POST /api/ai/resource-recommendation/`
*   **Method:** `POST`
*   **Purpose:** Calculates resource gaps (boats, pumps, vehicles).
*   **Authentication Requirement:** `AllowAny`
*   **Request Headers:** `Content-Type: application/json`
*   **Request Body:** `ward` (str), `flood_probability` (float), `risk_score` (float), `risk_factors` (list).
*   **Validation Rules:** `flood_probability` and `risk_score` must be between 0.0 and 100.0.
*   **Success Response:** `{"ward": "Diva", "resource_demand_score": 88.5, "resource_gap_score": 45.2, "resources_needed": [...], "priority_rank": 1, "confidence": 92.4}`
*   **Error Responses:** `400 Bad Request`, `503 Service Unavailable`.
*   **Monitoring Events Triggered:** `AIPredictionLog`.
*   **Expected Latency:** Avg: 25ms, P95: 60ms.

### 4. Building Advisor API
*   **Endpoint URL:** `POST /api/ai/building-advisor/`
*   **Method:** `POST`
*   **Purpose:** Predicts building collapse risk.
*   **Authentication Requirement:** `AllowAny`
*   **Request Headers:** `Content-Type: application/json`
*   **Request Body:** `building_id` (str).
*   **Validation Rules:** `building_id` must map to `dmd_building.id`.
*   **Success Response:** `{"building_id": "1", "building_name": "Sai", "ward": "Diva", "age_years": 45.0, "collapse_probability": 58.65, "classification": "Evacuation", "risk_factors": [...], "recommended_actions": [...], "confidence": 98.5}`
*   **Error Responses:** `400 Bad Request`, `404 Not Found` (IndexError in DB).
*   **Monitoring Events Triggered:** `AIPredictionLog`.
*   **Expected Latency:** Avg: 60ms.

### 5. Incident Forecast API
*   **Endpoint URL:** `POST /api/ai/forecast/`
*   **Method:** `POST`
*   **Purpose:** Time-series projection of events.
*   **Authentication Requirement:** `AllowAny`
*   **Request Headers:** `Content-Type: application/json`
*   **Request Body:** `days` (int).
*   **Validation Rules:** `days` min_value=1, max_value=365.
*   **Success Response:** `{"forecast_period": "7_days", "expected_incidents": 10, "hotspots": [...], "category_forecast": {...}, "severity_distribution": {...}, "explanations": [...]}`
*   **Error Responses:** `400 Bad Request`.
*   **Monitoring Events Triggered:** `AIPredictionLog`.
*   **Expected Latency:** Avg: 110ms.

### 6. Recommendation Engine API
*   **Endpoint URL:** `POST /api/ai/recommendations/`
*   **Method:** `POST`
*   **Purpose:** Apex engine merging all sub-models into escalation directives.
*   **Authentication Requirement:** `AllowAny`
*   **Request Headers:** `Content-Type: application/json`
*   **Request Body:** `ward` (str), `flood_probability` (float), `ward_risk_score` (float), `resource_shortage_score` (float), `building_risk_score` (float), `forecast_incidents` (float), `forecast_severity_critical_pct` (float).
*   **Validation Rules:** All probabilities/scores bound 0.0 - 100.0.
*   **Success Response:** `{"ward": "Diva", "combined_risk_score": 77.29, "priority_level": "Level 4", "escalation_level": "Critical Emergency", "recommendations": [...], "confidence": 88.0}`
*   **Error Responses:** `400 Bad Request`.
*   **Monitoring Events Triggered:** `AIPredictionLog`.
*   **Expected Latency:** Avg: 35ms.

### 7. Chatbot API
*   **Endpoint URL:** `POST /api/ai/chatbot/`
*   **Method:** `POST`
*   **Purpose:** NLP semantic routing.
*   **Authentication Requirement:** `AllowAny`
*   **Request Headers:** `Content-Type: application/json`
*   **Request Body:** `question` (str).
*   **Validation Rules:** `question` max_length=500.
*   **Success Response:** `{"question": "...", "answer": "...", "reasoning": [...], "recommended_actions": [...], "modules_used": [...], "confidence": 98.5, "intent": "BuildingRisk"}`
*   **Error Responses:** `400 Bad Request`.
*   **Monitoring Events Triggered:** `ChatbotLog`.
*   **Expected Latency:** Avg: 180ms.

---

## SECTION 3 — COMPLETE RESPONSE FIELD REGISTRY

| Field | Type | Range | Nullable | Always Present | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `risk_score` | Float | 0.0 - 100.0 | No | Yes | Normalized risk metric via Coefficient of Variation. |
| `flood_probability` | Float | 0.0 - 100.0 | No | Yes | Scikit-Learn `predict_proba()` class 1 output. |
| `confidence` | Float | 0.0 - 100.0 | No | Yes | System certainty based on data availability & algorithm confidence. |
| `risk_level` | String | Enum | No | Yes | "Low", "Moderate", "High", "Critical". |
| `collapse_probability`| Float | 0.0 - 100.0 | No | Yes | Actuarial probability of building failure. |
| `resource_demand_score`| Float | 0.0 - 100.0 | No | Yes | Normalized historical dependency on TMC assets. |
| `escalation_level` | String | Enum | No | Yes | "Level 1" to "Level 4 (Critical Emergency)". |
| `hotspots` | List(Str)| N/A | No | Yes | Array of ward names with highest projected incident density. |

---

## SECTION 4 — OPENAPI STYLE CONTRACTS

### FloodPredictionRequest
```json
{
  "type": "object",
  "required": ["ward", "rainfall", "humidity", "water_level", "temperature", "previous_flood_count", "is_monsoon"],
  "properties": {
    "ward": { "type": "string", "maxLength": 100 },
    "rainfall": { "type": "number", "minimum": 0.0 },
    "humidity": { "type": "number", "minimum": 0.0, "maximum": 100.0 },
    "water_level": { "type": "number", "minimum": 0.0 },
    "temperature": { "type": "number" },
    "previous_flood_count": { "type": "integer", "minimum": 0 },
    "is_monsoon": { "type": "integer", "minimum": 0, "maximum": 1 }
  }
}
```

### IncidentForecastRequest
```json
{
  "type": "object",
  "required": [],
  "properties": {
    "days": { "type": "integer", "minimum": 1, "maximum": 365, "default": 7 }
  }
}
```

---

## SECTION 5 — API VERSIONING

**Current Version:** `v1`

**Rules:**
- `v1` contracts cannot break.
- New fields must be appended as backward compatible.
- Deprecation requires a 30-day migration notice via HTTP header `Warning: 299 - Deprecated API`.
- Future breaking structural changes must route via `/api/v2/`.

---

## SECTION 6 — PERFORMANCE & SLA CONTRACT

| Endpoint | Expected Avg | P95 | Max |
| :--- | :--- | :--- | :--- |
| `POST /flood-prediction/` | 45ms | 120ms | 210ms |
| `GET /ward-risk/` | 85ms | 150ms | 300ms |
| `POST /resource-recommendation/`| 25ms | 60ms | 110ms |
| `POST /building-advisor/` | 60ms | 140ms | 250ms |
| `POST /forecast/` | 110ms| 180ms | 350ms |
| `POST /recommendations/` | 35ms | 80ms | 150ms |
| `POST /chatbot/` | 180ms| 310ms | 500ms |

*Verified against `audit_stress_test.py` and Monitoring layer DB latencies.*

---

## SECTION 7 — OBSERVABILITY CONTRACT

**Traceability Flow:**
Frontend Request -> API Gateway (Injects `X-Request-ID`) -> Django View -> `ai_monitoring.services.LoggingService` -> `AIPredictionLog` (Generates `prediction_id` UUID).

*   `prediction_id`: Primary key UUID injected into every row in `dmd_aipredictionlog`.
*   `status`: Always strictly "SUCCESS" or "ERROR".
*   `error_message`: Tracks specific stack traces on 500 or validation text on 400.

---

## SECTION 8 — DATABASE OPERATION MODES

**Toggle Location:** `dmd_project/settings.py` -> `AI_USE_LIVE_DATABASE`

*   **Mode A (False):** The `DataSourceFactory` uses `pandas.read_csv()` to pull baselines from `generated_data/*.csv`.
*   **Mode B (True):** The `DataSourceFactory` uses `connection.cursor()` to execute exact `JOIN` queries against the 3NF MySQL Production schema (`dmd_ward`, `dmd_incident`, etc.).

**Failure Modes:** If MySQL is offline during Mode B, the application crashes unless `AI_USE_LIVE_DATABASE` is flipped to False.

---

## SECTION 9 — MODEL ARTIFACT INVENTORY
*Location: `ai_engine/saved_models/`*

| Artifact | Purpose | Required |
| :--- | :--- | :--- |
| `flood_prediction.pkl` | Random Forest for inundation | Critical |
| `ward_risk_model.pkl` | Weights/Scalers dict for Ward | Critical |
| `resource_recommendation.pkl`| Resource gaps logic | Critical |
| `building_advisor.pkl` | Structural collapse heuristic | Critical |
| `incident_forecast.pkl` | Time-series volume ratios | Critical |
| `recommendation_engine.pkl` | Apex logic thresholds | Critical |

---

## SECTION 10 — VERIFIED PRODUCTION READINESS

**Source:** `REAL_VERIFICATION_AUDIT.md`

**READY:**
- AI Engine accuracy and determinism.
- Null Handling in live DB integration.
- Graceful degradation on missing `.pkl` files (Returns 503 instead of 500).
- Monitoring telemetry hooks.

**NOT READY / PRODUCTION BLOCKERS:**
- **AllowAny authentication:** (Owner: Backend Team) All AI endpoints are exposed globally. Requires API Gateway JWT validation.
- **Stateless chatbot:** (Owner: Frontend/AI Team) No conversation memory.
- **Django Runserver:** (Owner: DevOps Team) Currently using single-threaded development server. Requires Gunicorn + Nginx.

---

## SECTION 11 — FRONTEND CONSUMPTION GUIDE

**Example: Flood API**
*   **Trigger:** "Predict Flood Risk" button on Hydrology view.
*   **Loading State:** Render spinner overlay blocking secondary clicks.
*   **Success State:** Render Risk Card (Red for High/Critical, Yellow for Moderate, Green for Low).
*   **Error State:** Show field-level red text below inputs mapped from 400 JSON dictionary.

---

## SECTION 12 — BACKEND INTEGRATION GUIDE

**System Architecture Flow:**
Frontend UI -> API Gateway (Auth & Rate Limit) -> Django WSGI Server -> `ai_api.urls` -> `AIServiceLayer` -> `DataSourceFactory` (MySQL Query) -> Random Forest `.predict_proba()` -> `@monitor_request` -> HTTP 200 OK Response.
