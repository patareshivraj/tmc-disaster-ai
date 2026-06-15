# Resource Recommendation AI Architecture

## Overview
The Resource Recommendation AI is a decision-support engine designed to consume outputs from both the Flood Prediction AI and Ward Risk AI to determine operational logistics. It calculates priority rankings for all TMC wards and assigns specific emergency resources with exact quantities and actionable justifications.

## Inputs
1.  **Ward Risk AI:** Base risk score (0-100), Risk level, and specific risk factors.
2.  **Flood Prediction AI:** Flood probability (0-100%).
3.  **Historical Datasets:** `incidents.csv` and `resources.csv` to map historical resource burn rates per incident type.

## Core Engines
### 1. Resource Demand Engine
Calculates a `resource_demand_score` (0-100) using a blended formula:
- Flood Probability (40% weight)
- Overall Ward Risk Score (40% weight)
- Historical Incident Frequency Penalty (20% weight)

### 2. Priority Engine
Dynamically ranks all 9 wards in TMC by `resource_demand_score` to assign a relative Priority Rank (1 to 9). 

### 3. Allocation & Gap Engine
Defines specific resource allocations based on risk boundaries:
- **Water Pumps:** Driven primarily by Flood Probability thresholds.
- **Rescue Boats:** Allocated only in Critical/High flood probability scenarios.
- **Emergency Vehicles:** Driven by total Ward Risk and Incident History.
- **Structural Response Teams:** Allocated if "High Building Risk" is identified by Ward Risk AI.
- **Fire Tenders:** Baseline allocation for high generic risk levels.

### 4. Explainability Logic
For each recommended resource, a discrete justification is generated (e.g., `Critical flood probability (88%) requires immediate deployment of 5 pumps`).

## Outputs
JSON format strictly mapping to backend API expectations, including:
- Ward Name
- Priority Rank (1 to N)
- Resource Demand Score
- Array of `resources_needed` (type, quantity, reason)
- Array of `recommendations` (High-level tactical actions)
