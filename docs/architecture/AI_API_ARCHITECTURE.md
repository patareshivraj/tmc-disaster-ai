# Phase 13 AI API & Integration Layer Architecture

## Overview
The AI API Layer acts as the bridge between the internal AI Python engines and external systems (Dashboards, Mobile Apps, Command Centers). It is built using Django REST Framework and enforces strict separation of concerns through Views, Services, and Serializers.

## Data Flow
`Frontend Request` → `API View` → `Serializer Validation` → `Service Layer Orchestration` → `AI Engine Inference` → `JSON Response`

## Structural Components
1.  **Serializers (`ai_api/serializers.py`)**: Responsible for strict type-checking, bounds validation, and requirement enforcement on all incoming requests (e.g., ensuring `ward` is provided, `rainfall` cannot be negative).
2.  **Service Layer (`ai_api/services.py`)**: Responsible for instantiating the correct AI engine class, executing inference logic, catching model-level errors (e.g., FileNotFound or KeyError), and transforming raw DataFrames/dictionaries into clean, dashboard-ready JSON.
3.  **API Views (`ai_api/views.py`)**: Thin controllers handling HTTP request/response lifecycles and HTTP status code routing (400, 404, 500, 200).

## Endpoints

### 1. Universal Prediction API
*   **Method:** POST
*   **Endpoint:** `/api/ai/universal-prediction/`
*   **Input:** Ward context, weather variables.
*   **Output:** 360-degree threat matrix split into active weather threats and historical baseline risks.

### 2. Flood Prediction API
*   **Method:** POST
*   **Endpoint:** `/api/ai/flood-prediction/`
*   **Input:** Ward context, weather variables (rainfall, water level, etc.)
*   **Output:** Flood probability, risk level, confidence.

### 3. Fire Prediction API
*   **Method:** POST
*   **Endpoint:** `/api/ai/fire-prediction/`
*   **Input:** Ward context, temperature, humidity.
*   **Output:** Fire probability, severity, based on DB incident frequencies.

### 2. Ward Risk API
*   **Method:** GET
*   **Endpoint:** `/api/ai/ward-risk/{ward}/`
*   **Output:** Comprehensive vulnerability scoring and geographic risk matrices.

### 3. Resource Recommendation API
*   **Method:** POST
*   **Endpoint:** `/api/ai/resource-recommendation/`
*   **Input:** Ward, flood probability, ward risk score.
*   **Output:** Actionable resource deployments and identified equipment shortages.

### 4. Building Advisor API
*   **Method:** POST
*   **Endpoint:** `/api/ai/building-advisor/`
*   **Input:** Building ID.
*   **Output:** Collapse probability and structural audit requirements.

### 5. Incident Forecast API
*   **Method:** POST
*   **Endpoint:** `/api/ai/forecast/`
*   **Input:** Forecast window (days).
*   **Output:** Temporal incident trajectories and future ward hotspots.

### 6. Recommendation Engine API
*   **Method:** POST
*   **Endpoint:** `/api/ai/recommendations/`
*   **Input:** Payload aggregating Flood, Ward Risk, Shortages, and Forecasts.
*   **Output:** The apex priority score, escalation requirement, and generated operational actions.

### 8. Generative Copilot API
*   **Method:** POST
*   **Endpoint:** `/api/ai/copilot/`
*   **Input:** Natural language user query.
*   **Output:** Generative multi-agent reasoning utilizing Google Gemini 2.5 Flash.

### 9. Chatbot Intelligence API
*   **Method:** POST
*   **Endpoint:** `/api/ai/chatbot/`
*   **Input:** Natural language user query.
*   **Output:** Extracted intents via Legacy NLP.

## Error Handling Standards
*   `400 Bad Request`: Payload validation failures (e.g., missing fields).
*   `404 Not Found`: Entity missing (e.g., invalid Ward name or Building ID).
*   `422 Unprocessable Entity`: Math/AI logic execution failure due to conflicting inputs.
*   `500 Internal Server Error`: Hard model load failures or system crashes.
