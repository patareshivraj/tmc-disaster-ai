# TMC Disaster Management AI Platform — System Inventory

## 1. AI Modules
1.  **Flood Prediction Engine** (`ai_engine/models/flood_model.py`): Neural risk classifier based on meteorological variables.
2.  **Ward Risk Engine** (`ai_engine/models/ward_risk_model.py`): Vulnerability aggregator mapping historical socio-economic and demographic stress.
3.  **Resource Recommendation Engine** (`ai_engine/models/resource_recommendation_model.py`): Equipment calculation engine projecting deficits vs inventory.
4.  **Building Advisor Engine** (`ai_engine/models/building_advisor_model.py`): Structural risk analyzer mapping collapse probability logic.
5.  **Incident Forecast Engine** (`ai_engine/models/incident_forecast_model.py`): Time-series predictor charting near-term hotspots.
6.  **Recommendation Engine** (`ai_engine/models/recommendation_engine.py`): Apex AI fusing inputs from all 5 sub-AIs into Priority/Escalation thresholds.

## 2. Intelligence Layers
1.  **Chatbot Orchestrator** (`ai_engine/chatbot/`): NLP Multi-Agent router. Includes `intent_engine.py` (Semantics), `chatbot_orchestrator.py` (Routing), and `response_builder.py` (NLP Synthesis).
2.  **AI Service Layer** (`ai_api/services.py`): Singleton wrapper that loads all models centrally into memory to preserve performance.

## 3. Django REST API Layer (`ai_api/`)
1.  `/api/ai/flood-prediction/` (POST)
2.  `/api/ai/ward-risk/{ward}/` (GET)
3.  `/api/ai/resource-recommendation/` (POST)
4.  `/api/ai/building-advisor/` (POST)
5.  `/api/ai/forecast/` (POST)
6.  `/api/ai/recommendations/` (POST)
7.  `/api/ai/chatbot/` (POST)

## 4. Monitoring & Governance Layer (`ai_monitoring/`)
1.  **AIPredictionLog**: Database ledger capturing 100% of mathematical inferences, inputs, errors, and confidences.
2.  **ChatbotLog**: Database ledger capturing exact text, intents, and NLP response times.
3.  **AnalyticsService**: Extract service generating live usage metrics, error rates, and load averages.
4.  **AuditTrailEngine**: Forensic extraction engine for Government Commissioner reporting.

## 5. Saved Models & Data Artifacts
*   `saved_models/`: Contains the pre-trained pickled binaries supporting rapid offline inference.
*   `generated_data/`: Contains the synthetic TMC baseline CSVs representing physical world constraints.
