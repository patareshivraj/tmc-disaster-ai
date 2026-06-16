# TMC Disaster Management — AI Intelligence Layer

A production-grade AI platform for the **Thane Municipal Corporation (TMC)** that augments disaster management officers with data-driven predictions, risk scoring, resource optimization, and a conversational intelligence interface.

Built across **15 engineering phases** with rigorous audit cycles, this system provides a complete backend AI layer accessible through secure Django REST APIs.

---

## System Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    API Consumers                         │
│         Dashboard · Mobile App · Command Center          │
└──────────────────────┬───────────────────────────────────┘
                       │  HTTP/JSON
┌──────────────────────▼───────────────────────────────────┐
│              Django REST API Layer (ai_api/)              │
│     Serializers → Views → Service Layer → AI Engines     │
├──────────────────────────────────────────────────────────┤
│              AI Engine Layer (ai_engine/)                 │
│                                                          │
│  ┌─────────────┐ ┌─────────────┐ ┌────────────────────┐ │
│  │  Flood AI   │ │ Ward Risk   │ │ Resource Optimizer │ │
│  │ (Random     │ │ (CV-Derived │ │ (Data-Driven       │ │
│  │  Forest)    │ │  Scoring)   │ │  Coefficients)     │ │
│  └─────────────┘ └─────────────┘ └────────────────────┘ │
│  ┌─────────────┐ ┌─────────────┐ ┌────────────────────┐ │
│  │ Building    │ │ Incident    │ │ Recommendation     │ │
│  │ Advisor     │ │ Forecast    │ │ Engine             │ │
│  │ (Actuarial) │ │ (Seasonal)  │ │ (Multi-AI Fusion)  │ │
│  └─────────────┘ └─────────────┘ └────────────────────┘ │
│  ┌──────────────────────────────────────────────────────┐│
│  │         Chatbot Intelligence Layer                   ││
│  │   TF-IDF Intent Detection → Orchestrator → NLG      ││
│  └──────────────────────────────────────────────────────┘│
├──────────────────────────────────────────────────────────┤
│           Monitoring & Audit Layer (ai_monitoring/)       │
│     Prediction Logs · Chatbot Logs · Analytics · Audit   │
└──────────────────────────────────────────────────────────┘
```

---

## AI Modules

| Module | Type | Input | Output |
| :--- | :--- | :--- | :--- |
| **Flood Prediction** | Random Forest Classifier (SMOTE) | Weather variables, ward | Flood probability, risk level |
| **Ward Risk** | Data-derived scoring (CV weights) | Ward name | Risk score, factors, recommendations |
| **Resource Optimizer** | Coefficient-based allocation | Ward, flood prob, risk score | Equipment needs, shortage analysis |
| **Building Advisor** | Actuarial risk model (P-Union) | Building ID | Collapse probability, classification |
| **Incident Forecast** | Seasonal extrapolation | Forecast window (days) | Expected incidents, hotspots |
| **Recommendation Engine** | Multi-AI fusion | All sub-AI outputs | Priority level, actions, escalation |
| **Chatbot** | TF-IDF + Cosine Similarity | Natural language question | Answer, reasoning, actions |

---

## API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/ai/flood-prediction/` | POST | Predict flood risk for a ward |
| `/api/ai/ward-risk/{ward}/` | GET | Get comprehensive ward vulnerability |
| `/api/ai/resource-recommendation/` | POST | Calculate resource needs and shortages |
| `/api/ai/building-advisor/` | POST | Assess structural risk by building ID |
| `/api/ai/forecast/` | POST | Forecast incident volume and hotspots |
| `/api/ai/recommendations/` | POST | Generate prioritized officer actions |
| `/api/ai/chatbot/` | POST | Ask questions in natural language |

---

## Quick Start

```bash
# Clone
git clone https://github.com/patareshivraj/tmc-disaster-ai.git
cd tmc-disaster-ai

# Virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# Dependencies
pip install -r requirements.txt

# Database
python manage.py migrate

# Train AI models (first time only)
python ai_engine/training/train_flood_model.py
python ai_engine/training/train_ward_risk.py
python ai_engine/training/train_resource_model.py
python ai_engine/training/train_building_model.py
python ai_engine/training/train_forecast_model.py
python ai_engine/training/train_recommendation_engine.py

# Run server
python manage.py runserver
```

---

## Project Structure

```
├── accounts/                    # Django auth
├── ai_api/                      # REST API (views, serializers, services)
├── ai_engine/
│   ├── chatbot/                 # TF-IDF intent engine, orchestrator, NLG
│   ├── features/                # Feature engineering pipelines
│   ├── models/                  # 6 AI model classes
│   ├── saved_models/            # Trained .pkl artifacts + metrics
│   ├── seeds/                   # Data generation scripts
│   └── training/                # Model training scripts
├── ai_monitoring/               # Prediction logs, analytics, audit trail
├── disaster/                    # Core disaster management app
├── dmd_project/                 # Django settings, urls
├── generated_data/              # Synthetic CSV/JSON datasets
├── tests/                       # API, monitoring, scenario, stress tests
├── docs/
│   ├── architecture/            # System, API, module design docs
│   ├── audits/                  # Phase audit & implementation reports
│   └── reports/                 # Completion, scoring, certification
├── manage.py
├── requirements.txt
└── README.md
```

---

## Testing

```bash
# API validation
python tests/test_api.py

# Monitoring validation
python tests/test_monitoring.py

# Demo scenarios (Flood, Building, Resource, City-Wide)
python tests/test_scenarios.py

# Independent stress test
python tests/audit_stress_test.py
```

---

## Tech Stack

- **Backend:** Django 6.0, Django REST Framework
- **ML:** scikit-learn, imbalanced-learn (SMOTE), joblib
- **NLP:** TF-IDF Vectorization + Cosine Similarity
- **Data:** pandas, numpy
- **Database:** SQLite (dev) / MySQL (production)

---

## Documentation

- **Architecture:** [`docs/architecture/`](docs/architecture/) — System design, data contracts, module specifications
- **Audits:** [`docs/audits/`](docs/audits/) — Phase-by-phase audit and implementation reports
- **Reports:** [`docs/reports/`](docs/reports/) — Project completion, scoring, production certification

---

## License

This project was developed as part of a Master's dissertation for the Thane Municipal Corporation Disaster Management Division.
