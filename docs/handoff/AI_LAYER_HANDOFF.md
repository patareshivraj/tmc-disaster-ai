# AI LAYER HANDOFF

**Date:** June 16, 2026
**Version:** v1.0.0-ai-layer

This document serves as the final integration boundary definition for the TMC Disaster Management AI Platform.

The AI engineering phase is now officially complete. The system has been packaged as a headless, deterministic intelligence microservice. 

## What the AI Team Owns & Has Delivered
* **Core Models:** 6 trained Random Forest / NLP models (`saved_models/*.pkl`) handling floods, resources, building risk, and intent detection.
* **API Layer:** 7 RESTful endpoints enforcing strict JSON schemas (documented in `FRONTEND_HANDOFF.md` and `sample_requests/`).
* **Database Adapters:** The `DataSourceFactory` which seamlessly bridges AI feature pipelines with the 3NF MySQL production schema.
* **Audit & Monitoring:** Automated telemetry via `@monitor_request` logging all executions to `AIPredictionLog` and `ChatbotLog`.
* **Reliability:** Built-in fault tolerance. Missing model files now gracefully degrade with HTTP 503 rather than crashing the Django application framework.

## What the Backend / Platform Team Owns
The AI repository must be securely integrated into the broader TMC ecosystem.
* **Authentication:** Implement JWT, OAuth, or static Bearer Tokens. The endpoints are currently `[AllowAny]`.
* **API Gateway & Rate Limiting:** Prevent DDoS attacks on computationally heavy endpoints.
* **Production Deployment:** Containerize the repository using Docker, configure Gunicorn/uWSGI for concurrent requests, and set up an Nginx reverse proxy.
* **Continuous Integration:** Configure GitHub Actions for automated regression testing on PRs.

## What the Frontend Team Owns
* **Command Center Dashboard:** Real-time visualization of `ward_risk` and `flood_probability` over mapped SVGs.
* **Chatbot UI:** A chat interface consuming the `/api/ai/chatbot/` endpoint.
* **Error Handling:** Gracefully parse HTTP 400 and HTTP 503 JSON responses to provide actionable feedback to dispatch operators.

## Known Limitations
1. **Stateless Chatbot:** The NLP intent router does not currently maintain conversational memory (e.g., follow-up questions require full context).
2. **Synthetic Bootstrapping:** AI models were trained on generated historical baselines. Real TMC data will slowly recalibrate confidence intervals over time.
3. **Artifact Dependency:** The repository relies on `.pkl` files in `ai_engine/saved_models/`. They must not be excluded during Docker builds.

## Future Enhancements (Phase 2 Roadmap)
* **LLM Integration:** Upgrading the TF-IDF intent router to a lightweight LLM (Llama 3 or similar) for conversational memory.
* **Automated Retraining:** Implementing an Airflow DAG to retrain the Random Forests nightly against live MySQL updates.
* **Geo-Spatial Features:** Adding GIS coordinate parsing for sub-ward level granularity.

---
**Sign-off:** The AI Layer is structurally complete, documented, resilient, and ready for production consumption.
