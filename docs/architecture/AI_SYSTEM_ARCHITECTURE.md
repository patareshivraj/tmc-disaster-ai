# TMC Disaster Management AI Layer — System Architecture

This document serves as the master architectural blueprint for the internal workings, data flows, and infrastructure design of the AI Layer within the Thane Municipal Corporation (TMC) Disaster Management platform. It outlines the modular components that will execute predictions, recommendations, forecasting, and conversational intelligence.

---

## 1. Overall AI System Architecture

The AI Layer acts as a decoupled intelligence hub. It consumes raw data from the TMC backend, processes it through feature engineering pipelines, executes machine learning inference, and returns actionable recommendations via a dedicated REST API.

**Architecture Flow:**
```text
[ TMC Database ] (Incident, Weather, Resources, Buildings)
       ↓
[ AI Feature Store / Data Extraction Layer ] (SQL/ORM queries, Aggregations)
       ↓
[ Feature Engineering Layer ] (Imputation, Scaling, Encoding, Rolling Averages)
       ↓
[ AI Engine Layer ] (ML Inference, Forecasting Models, Rule-Based Fallbacks)
       ↓
[ Recommendation Generator ] (Translates ML outputs to Officer Action Plans)
       ↓
[ AI Logging System ] (Records Predictions, Inputs, Confidences for Audit)
       ↓
[ Django REST API Layer ] (Serializes data to JSON)
       ↓
[ Consumer Applications ] (TMC Officer Dashboards, Mobile Apps)
```

**Responsibilities:**
*   **Feature Layer:** Transforms raw database records into normalized mathematical inputs suitable for ML models.
*   **AI Engines:** Executes models (XGBoost, Prophet, etc.) to calculate risks, probabilities, and forecasts.
*   **Recommendation Layer:** Maps statistical outputs to human-readable actions (e.g., "Deploy 2 Pumps").
*   **API Layer:** Handles authentication, rate limiting, and structured JSON delivery of insights.

---

## 2. Universal Threat Prediction Architecture

**Goal:** Predict imminent risks across ALL 12 disaster categories based on live weather constraints and database incident histories.

*   **Input Datasets:** Live MySQL Database (`dmd_disaster_category`, `dmd_incident`), Weather Payload.
*   **API:** `POST /api/ai/universal-prediction/`

**Architecture Diagram:**
```text
Environmental Data Payload (Temp, Rainfall, Humidity)
       ↓
Dynamic SQL Category Discovery
       ↓
Historical Incident Baseline Engine (Counts ward-specific frequencies)
       ↓
Active Weather Heuristic Engine (Overlays physics constraints)
       ↓
Universal Threat Matrix
       ↓
API Response (Separated into Active Threats vs Baseline Risks)
```

**Definitions:**
*   **Inputs:** `rainfall`, `water_level`, `temperature`, `humidity`, `is_monsoon`, `ward`
*   **Processing Flow:** Parse inputs -> Query DB for categories -> Calculate historical baselines -> Apply weather heuristics (e.g., if temp > 40C, Heat Wave risk spikes) -> Sort by severity.
*   **Outputs:** 360-degree risk array for 12+ disasters.

---

## 3. Flood Prediction Architecture

**Goal:** Predict imminent flood risks based on weather conditions and geographical vulnerability.

*   **Input Datasets:** Weather Dataset, Incident Dataset, Ward Dataset
*   **Future API:** `POST /api/ai/flood-prediction/`

**Architecture Diagram:**
```text
Current Weather Data + Historical Floods
       ↓
Feature Engineering (Rolling averages of rainfall, alert encoding)
       ↓
Flood Prediction ML Engine (Classification for Risk, Regression for Probability)
       ↓
Risk Score & Probability Matrix
       ↓
Recommendation Generator (Action thresholds based on Risk)
       ↓
API Response (Risk Level + Actions)
```

**Definitions:**
*   **Inputs:** `rainfall_mm`, `water_level_m`, `ward_id`, `alert_level`
*   **Processing Flow:** Parse inputs -> Fetch 3-day rainfall moving average -> Execute Model -> Map score to risk bracket -> Lookup standard actions for bracket.
*   **Outputs:** Risk Level (Low/Med/High/Critical), Probability (0-100%)
*   **Recommendations:** Evacuation advisories, Pump deployments, Alert issuances.
*   **Future ML Models:** XGBoost Classifier, Random Forest.
*   **Rule-Based Alternative:** If `rainfall_mm` > 120 and `water_level` > Danger Mark -> Critical Risk.

---

## 3. Ward Risk Analysis Architecture

**Goal:** Provide a strategic, long-term vulnerability score for resource planning across all 9 wards.

*   **Input Datasets:** Incident Dataset, Preparedness Dataset, Weather Dataset
*   **Future API:** `GET /api/ai/ward-risk/`

**Architecture Diagram:**
```text
Historical Incidents + Preparedness Programs
       ↓
Risk Scoring Layer (Aggregates severity, normalizes by population)
       ↓
Vulnerability Engine (K-Means / Weighted Scoring)
       ↓
Ward Risk Profile (0-100 Score, Risk Tier)
       ↓
Strategic Recommendation Layer
       ↓
API Response
```

**Definitions:**
*   **Inputs:** Historical incident frequency, average severity, preparedness drill counts per ward.
*   **Processing Flow:** Aggregate last 12 months data -> Apply penalty for severe incidents -> Apply discount for preparedness drills -> Normalize score 0-100.
*   **Outputs:** Risk Score, Risk Level, Primary Reasons.
*   **Recommendations:** Infrastructure upgrades, mandatory citizen drills, budget allocation priorities.
*   **Future ML Models:** K-Means Clustering (to group similar wards), Ridge Regression.
*   **Rule-Based Alternative:** Weighted sum logic based on disaster categories.

---

## 4. Resource Recommendation Architecture

**Goal:** Suggest exact resource counts needed to handle an active incident efficiently.

*   **Input Datasets:** Incident Dataset, Resource Usage Dataset, Response Team Dataset
*   **Future API:** `POST /api/ai/resource-recommendation/`

**Architecture Diagram:**
```text
Active Incident Details (Type, Severity, Ward)
       ↓
Historical Similarity Matching
       ↓
Resource Recommendation ML Engine
       ↓
Predicted Resource Array (Boats, Pumps, Vehicles, Teams)
       ↓
Inventory Check (Optional cross-reference with Team Availability)
       ↓
API Response
```

**Definitions:**
*   **Inputs:** `incident_type`, `severity`, `ward`
*   **Processing Flow:** Extract features -> Find top N historically similar resolved incidents -> Average resources used -> Round to nearest integer.
*   **Outputs:** Required number of Teams, Boats, Pumps, Vehicles.
*   **Recommendations:** Specific dispatch plans.
*   **Future ML Models:** K-Nearest Neighbors (KNN), Multi-output LightGBM.
*   **Rule-Based Alternative:** Static matrix mapping incident type and severity to fixed resource counts.

---

## 5. Building Advisor Architecture

**Goal:** Prescribe safety and structural actions for dilapidated buildings.

*   **Input Datasets:** Building Dataset, Inspection Dataset, Risk Dataset
*   **Future API:** `GET /api/ai/building-advice/`

**Architecture Diagram:**
```text
Building Profile (Age, Condition, Ward, Risk Level)
       ↓
Feature Engineering (Age categorization, Condition encoding)
       ↓
Building Safety ML Advisor
       ↓
Action Classifier (Monitor, Repair, Demolish, etc.)
       ↓
Justification Generator
       ↓
API Response
```

**Definitions:**
*   **Inputs:** `building_age`, `condition`, `inspection_date`, `risk_level` (C1-C4)
*   **Processing Flow:** Parse building stats -> Evaluate against historical collapse data -> Determine highest-probability safe action -> Generate explanation.
*   **Outputs:** Recommended Action, Urgency Level.
*   **Recommendations:** Evacuate immediately, schedule repair, monitor quarterly.
*   **Future ML Models:** Support Vector Machines (SVM), Logistic Regression.
*   **Rule-Based Alternative:** Direct mapping from TMC C1-C4 guidelines.

---

## 6. Incident Forecast Architecture

**Goal:** Estimate the volume of disasters in upcoming months to aid proactive readiness.

*   **Input Datasets:** Historical Incident Dataset, Weather Dataset, Seasonal Dataset
*   **Future API:** `GET /api/ai/forecast/`

**Architecture Diagram:**
```text
Time-Series Incident Data (2018-Current)
       ↓
Seasonality Extraction Layer
       ↓
Time-Series Forecasting Engine (Prophet / SARIMA)
       ↓
Predicted Incident Counts per Ward/Type
       ↓
Alert Flagging (Identify spikes)
       ↓
API Response
```

**Definitions:**
*   **Inputs:** Timeframe (e.g., Next 30 days), Historical records.
*   **Processing Flow:** Load historical aggregated monthly data -> Identify trends & seasonality -> Project n-steps ahead -> De-aggregate to ward level.
*   **Outputs:** Forecasted counts for Flood, Fire, Tree Fall, etc.
*   **Forecasts:** High-risk ward identifications for the upcoming period.
*   **Future ML Models:** Facebook Prophet, LSTM Networks, SARIMA.
*   **Rule-Based Alternative:** Moving average of the same month across the previous 3 years.

---

## 8. Generative Copilot Architecture

**Goal:** Provide an autonomous agentic interface to interact with all underlying AI models via natural language.

*   **Components:** Google Gemini 2.5 Flash, OpenAI Compatibility Layer, Tool Router.
*   **API:** `POST /api/ai/copilot/`

**Architecture Diagram:**
```text
User Natural Language Query
       ↓
Gemini 2.5 Flash LLM (Reasoning Engine)
       ↓
Tool Calling Logic (JSON Schemas)
       ↓
Tool Router Executes Deterministic Model (e.g. Universal Prediction)
       ↓
Context Builder (Merges DB results + AI predictions)
       ↓
LLM Synthesizes Officer-Ready Response
       ↓
API Response
```

**Definitions:**
*   **LLM Provider:** Google Gemini via `generativelanguage.googleapis.com` (Groq is deprecated).
*   **Tool Router:** Connects the LLM directly to `AIServiceLayer` methods without manual intervention.
*   **Prompt Management:** Strict system instructions enforce municipal guidelines and prevent hallucination.

---

## 9. AI Service Layer Structure

The business logic of the AI Layer is isolated in the `services/` directory. 

*   `flood_prediction.py`: Executes data fetching, runs flood ML models, generates action lists.
*   `ward_risk_analysis.py`: Aggregates ward statistics, calculates vulnerability scores.
*   `resource_recommendation.py`: Matches historical events, outputs resource arrays.
*   `building_advisor.py`: Evaluates structural parameters, classifies safety actions.
*   `incident_forecast.py`: Handles time-series logic, returns projected timelines.
*   `chatbot_service.py`: Manages the LLM lifecycle, prompt injection, and intent routing.

**Dependencies:** Services operate independently. `chatbot_service.py` may internally invoke other services to answer complex queries (e.g., invoking `flood_prediction.py` if asked "Is Kalwa safe today?").

---

## 9. AI API Layer Design

The interface to the outside world is handled via Django REST Framework in `ai_engine/api/`.

*   `urls.py`: Maps external HTTP requests to internal views.
*   `views.py`: Acts as the controller. Validates the request, calls the appropriate service from `services/`, and formats the response.
*   `serializers.py`: Ensures input validation (e.g., checking that `rainfall_mm` is a positive float) and structures JSON output.

**Flow:** Request -> URL Router -> DRF Serializer (Validation) -> API View -> AI Service (Logic/ML) -> DRF Serializer (Formatting) -> HTTP JSON Response.
**Error Handling Strategy:** Standardized JSON error responses (400 Bad Request for validation failures, 500 Internal Server Error for model failures).

---

## 10. AI Logging & Monitoring Architecture

To ensure model transparency, explainability, and auditability for government stakeholders.

**Future Table Schemas (`ai_prediction_logs`):**
*   `log_id` (UUID)
*   `timestamp` (DateTime)
*   `module_name` (String: e.g., "Flood Prediction")
*   `request_payload` (JSON)
*   `input_features` (JSON: Post-feature-engineering state)
*   `prediction_output` (JSON)
*   `confidence_score` (Float)
*   `explainability_notes` (Text: E.g., "Risk triggered due to 3-day rainfall > 200mm")
*   `actual_outcome` (JSON: Populated later to track model drift and accuracy)

Logs will be written asynchronously to avoid slowing down API responses.

---

## 11. Feature Engineering Layer

**Strategy:** Transform raw relational data into ML-ready formats prior to inference.

*   **Raw Inputs:** Standard database records.
*   **Derived Features:** `building_age` (Current Year - `year_built`), `rolling_3day_rainfall` (Sum of last 3 days).
*   **Feature Transformations:** One-hot encoding for `ward`, Label encoding for `severity`, Min-Max scaling for continuous variables (`water_level_m`).
*   **Feature Storage Strategy:** Calculated on-the-fly for real-time predictions; cached in memory (Redis) for frequent batch predictions (like Ward Risk).
*   **Future Feature Store Design:** If the system scales, a dedicated Feature Store (e.g., Feast) will be introduced to maintain consistency between training and inference environments.

---

## 12. Future Model Registry

**Goal:** Manage lifecycle and versioning of pickled ML models.

**Architecture:**
*   **Storage:** AWS S3 or Local File System (`models/bin/`).
*   **Metadata DB:** Tracks `model_id`, `module_name`, `version`, `training_date`, `accuracy_f1_score`, `status` (Active, Shadow, Retired).
*   **Deployment Status:** Allows A/B testing or silent shadow-mode deployments.
*   **Rollback Strategy:** If a model's real-world accuracy drops (data drift), the service layer automatically points to the previous stable `version`.

---

## 13. Future Deployment Architecture

**Flow:**
```text
[ TMC MySQL Database ]
       ⬍
[ AI Django Backend (Docker Container) ] -> [ Redis Cache ] -> [ Model S3 Bucket ]
       ⬍
[ Reverse Proxy (Nginx) / Load Balancer ]
       ⬍
[ Front-End Dashboards / External Government Systems ]
```

**Considerations:**
*   **Scalability Considerations:** The AI Django backend will be containerized using Docker, allowing Kubernetes to spin up multiple pods during high-traffic monsoons.
*   **Future Cloud Deployment:** Hosted on scalable VMs (e.g., AWS EC2 or Azure VMs) configured for data locality and government compliance.
*   **Monitoring & Performance:** Integration with Prometheus/Grafana to track ML inference times and API latency. Model accuracy tracking via the AI Logging Architecture.
