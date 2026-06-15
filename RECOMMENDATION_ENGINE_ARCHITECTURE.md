# Recommendation Engine AI Architecture

## Overview
The Recommendation Engine acts as the absolute apex of the TMC Disaster Management AI Layer. It does not predict future states; instead, it consumes the intelligence matrix output by all 5 sub-AIs (Flood, Ward Risk, Resource, Building, Forecast) to generate deterministic, officer-ready operational actions.

## 1. Feature Engineering
The engine fuses sub-AI inputs into composite operational scores:
*   `combined_risk_score`: Weighted multi-variate statistical sum of Flood, Ward, and Building risks.
*   `operational_stress_score`: Derived mathematically from `forecast_incidents` and `forecast_severity_critical_pct`.
*   `escalation_score`: Multiplies the `combined_risk_score` by the `resource_shortage_score` (representing the inability to mitigate an ongoing hazard).

## 2. Priority Engine
Assigns standard TMC classifications: `Low`, `Moderate`, `High`, `Critical`, `Extreme`.
This classification is **Data-Driven**. The training module analyzes historical datasets to calculate the standard deviation bounds of normal ward operational stress. A "Critical" priority strictly means the `combined_risk_score` exceeds the 95th percentile of historical disaster baselines.

## 3. Escalation Engine
Determines bureaucratic hierarchy routing. 
- `No Action` -> `Monitor` -> `Department Action` -> `Emergency Action` -> `Control Room Escalation` -> `Commissioner Escalation`.
Escalation emerges probabilistically from the `escalation_score`. (e.g., High disaster probability + Zero resources = Control Room Escalation).

## 4. Action Recommendation Engine
Orchestrates specific deployment logic by cross-referencing thresholds. Rather than using fixed `if` statements, the engine builds an internal "Action Confidence Matrix".
For example, the action "Deploy Pumps" receives a confidence score mathematically mapped to the normalized product of `flood_probability` and `resource_shortage_score`. The engine selects the Top N actions whose confidence > acceptable threshold.

## 5. Explainability Layer
Explanations are strictly bound to the explicit sub-AI inputs that drove the confidence matrix above its threshold. (e.g., `"Deploy Pumps selected due to Flood Probability [88%] overlapping Resource Shortage [82%]"`).
