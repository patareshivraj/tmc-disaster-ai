# Incident Forecast AI Architecture

## Overview
The Incident Forecast AI is a data-driven time-series engine designed to predict future disaster occurrences across the Thane Municipal Corporation. By analyzing historical incidents (`incidents.csv`) and weather patterns (`weather.csv`), the AI extracts empirical seasonality, trend multipliers, and ward vulnerabilities to forecast "What, Where, When, and How Severe" upcoming incidents will be.

## Feature Engineering Layer
1.  **Temporal Decomposition:** Converts historical `incident_date` values into statistical `month` and `season` distributions to learn empirical baseline occurrence rates.
2.  **Category Aggregation:** Learns the historical proportion of incident categories (Flood, Fire, Tree Fall, etc.) relative to the time of year.
3.  **Severity Distributions:** Learns the baseline ratio of `Low`, `Medium`, `High`, `Critical` incidents historically reported for the requested period.
4.  **Hotspot Mapping:** Calculates a dynamic `hotspot_score` for each ward based on historical density, scaled by current weather patterns.

## Core Forecasting Engine
Instead of utilizing arbitrary or hardcoded "monsoon rules", the Forecasting Engine calculates a mathematically sound **Expected Volume**:
`Expected Incidents = Base Daily Rate × Forecast Window (days) × Seasonality Coefficient × Weather Trend Multiplier`

### 1. Seasonality Analysis
The model groups the entire historical dataset by `month` to calculate a `Seasonality Multiplier` representing how much higher or lower incident volume is expected compared to the annualized baseline.

### 2. Category & Severity Forecaster
Uses historical distribution matrices for the predicted time window to proportion the `Expected Incidents` into precise numerical categories. If historical data for June shows 70% floods, the engine will strictly forecast 70% of its volume as floods.

### 3. Hotspot Engine
Extracts the Top 5 most vulnerable wards using a data-driven rank of historical incident density blended with forward-looking modifiers.

### 4. Explainability Engine
Generates an explicit array of `explanations` citing the exact empirical coefficients used (e.g., `"Historical seasonality multiplier for the upcoming period is 1.45x normal volume."`).

## Output Schema
JSON response ready for APIs and the TMC Command Center Dashboard, exposing `forecast_period`, `expected_incidents`, `hotspots`, `category_forecast`, `severity_distribution`, and data-backed `explanations`.
