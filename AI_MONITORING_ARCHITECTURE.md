# Phase 14 AI Monitoring, Logging & Audit Layer Architecture

## Overview
The Phase 14 Monitoring Layer injects strict government-grade observability into the TMC Disaster Management AI platform. It tracks all AI transactions in real-time without modifying the underlying inferencing math or causing noticeable overhead latency.

## Architecture & Flow
```text
[ User / Command Center ]
       ↓ HTTP Request
[ AI API Views (`ai_api/views.py`) ]
       ↓ @monitor_request Decorator Intercept
[ AI Engine Inference ]
       ↓ Result Returned
[ AI Monitoring Service (`ai_monitoring/services.py`) ]
       ↓ Database Commit (Async-ready, SQLite default)
[ AIPredictionLog / ChatbotLog Table ]
       ↓
[ Audit Trail & Analytics (`ai_monitoring/audit.py`, `ai_monitoring/analytics.py`) ]
```

## Core Components
### 1. `ai_monitoring.models`
Defines the database schema required for long-term audit storage.
*   **`AIPredictionLog`**: General purpose ledger capturing API Endpoints, Input JSONs, Output JSONs, Confidence Scores, Error Strings, and strict execution latencies.
*   **`ChatbotLog`**: Specialized ledger specifically designed to monitor Conversational Intelligence. Captures the NLP Intent, natural language Question/Answer, and a complete trace of `modules_used` required to generate the response.

### 2. `ai_monitoring.services`
Handles the immediate I/O of inserting predictions into the database cleanly, removing logic weight from standard views. Provides `log_prediction` and `log_chatbot`.

### 3. `ai_monitoring.analytics`
Aggregates logs dynamically to generate high-level dashboards.
*   Tracks *Daily* and *Weekly Usage*.
*   Computes the *Average Response Time* and *Module Distribution* across the system.
*   Maintains an active *Error Rate* percentage gauge.

### 4. `ai_monitoring.audit`
Extracts point-in-time exact representations of historical AI actions using UUID lookups. Essential for producing reports during investigations (e.g., "Why was Mumbra ranked critical on August 15th?").

## Data Security & Privacy Strategy
*   **No Sensitive Stack Traces**: Stack traces are caught and converted to clean string errors (e.g. `ValueError`) before logging, ensuring database contents never leak codebase internal paths.
*   **Audit-Safe Persistence**: Log records capture AI logic paths (e.g. Confidence and Modules Used) rather than relying on external API analytics which can lack context.

## Log Retention Strategy
*   **7-Day Operational Logs**: Hot access for Command Center Dashboards.
*   **30-Day Archival Logs**: Incident post-mortem review timelines.
*   **90-Day Cold Storage**: Kept for seasonal compliance reporting, strictly purged after the monsoon cycle to preserve DB performance.
