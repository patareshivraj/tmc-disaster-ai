# DEPENDENCY AUDIT

**Date:** June 16, 2026
**Objective:** Purge transitive dependencies and define a strict, minimal manifest for production.

| Package | Used By | Required? | Keep / Remove | Reason |
| :--- | :--- | :--- | :--- | :--- |
| `Django` | Core | Yes | **Keep** | Web framework base. |
| `djangorestframework` | `ai_api` | Yes | **Keep** | REST interface layer. |
| `pandas` | `ai_engine`, `features` | Yes | **Keep** | Data manipulation and matrix formulation. |
| `scikit-learn` | `ai_engine/models` | Yes | **Keep** | Random Forest, TF-IDF NLP vectorization. |
| `imbalanced-learn` | `ai_engine/training` | Yes | **Keep** | SMOTE generation for Flood AI. |
| `joblib` | `ai_engine/models` | Yes | **Keep** | Model serialization/deserialization. |
| `mysqlclient` | `ai_engine/repositories` | Yes | **Keep** | Fast MySQL driver for Pandas/Django integration. |
| `numpy` | `ai_engine` | Yes | **Keep** | Core numerical calculations (often implied by Pandas but explicit is better). |
| `python-dotenv` | `dmd_project/settings.py` | Yes | **Keep** | Secure environment variable injection. |
| `asgiref` | Django (Transitive) | No | **Removed** | Will be installed automatically by Django. |
| `sqlparse` | Django (Transitive) | No | **Removed** | Will be installed automatically by Django. |
| `tzdata` | Django (Transitive) | No | **Removed** | Will be installed automatically by Django. |
| `python-dateutil` | Pandas (Transitive) | No | **Removed** | Will be installed automatically by Pandas. |
| `scipy` | Scikit-learn (Transitive) | No | **Removed** | Will be installed automatically by Scikit-Learn. |
| `threadpoolctl` | Scikit-learn (Transitive)| No | **Removed** | Will be installed automatically by Scikit-Learn. |
| `narwhals` | Pandas (Transitive) | No | **Removed** | Will be installed automatically by Pandas. |
| `six` | Dateutil (Transitive) | No | **Removed** | Will be installed automatically. |
| `sklearn-compat` | Imbalanced-learn | No | **Removed** | Will be installed automatically. |

**Result:** `requirements.txt` was reduced from 18 mixed packages down to 9 explicitly required, top-level libraries.
