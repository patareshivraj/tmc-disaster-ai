# Building Advisor AI Architecture

## Overview
The Building Advisor AI serves as the core intelligence engine for the Dangerous Buildings Dashboard and Structural Risk tracking. It evaluates individual structures across TMC by blending historical inspections, geographical exposure (weather/floods), and structural deterioration to output a `building_risk_score`, `collapse_probability`, and actionable municipal recommendations.

## Inputs
1.  **Buildings Dataset:** `building_age`, `structural_condition`, `risk_level`, `inspection_date`.
2.  **Incidents Dataset:** Maps local historical incidents (fires, floods) to the building's ward to determine baseline neighborhood exposure.
3.  **Weather Dataset:** Determines extreme weather and rainfall exposure specific to the building's geographic location.

## Engineered Features
- `building_age`: Current Year (2026) - `year_built`
- `years_since_last_inspection`: Current Year - `inspection_year`
- `structural_condition_score`: Numerical encoding of the inspection `condition` text.
- `flood_exposure_score`: Aggregate density of flood incidents in the building's ward.
- `fire_exposure_score`: Aggregate density of fire incidents in the building's ward.
- `maintenance_risk_score`: Derived scalar based on the ratio of `building_age` to `inspection_frequency`.

## Core Engines
### 1. Building Risk Engine
Computes `building_risk_score` (0-100) using a data-driven hybrid equation. The model leverages coefficients learned from `buildings.csv` relating age and structural condition to actual incidents.

### 2. Collapse Probability Engine
Estimates a strict `collapse_probability` (0-100%) using non-linear thresholds:
- Exponential decay applied for buildings > 50 years old.
- Multiplier added for "Poor" structural condition.
- Modifier added for > 3 years since the last inspection.

### 3. Safety Classification Engine
Determines the official TMC designation:
- `0–25`: Safe
- `26–50`: Monitor
- `51–70`: Repair Recommended
- `71–85`: Structural Audit Required
- `86–100`: Evacuation / Demolition Candidate

### 4. Recommendation & Explainability Engine
Generates explicit `risk_factors` (e.g., `"Age > 50 Years"`, `"Repeated Flood Exposure"`) and strict municipal actions (e.g., `"Immediate Evacuation"`, `"Structural Audit"`).

## Output Schema
JSON response ready for APIs/Dashboards containing `building_id`, `building_name`, `ward`, `risk_score`, `collapse_probability`, `classification`, `risk_factors`, and `recommendations`.
