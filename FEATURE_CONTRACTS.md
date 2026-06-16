# FEATURE CONTRACTS

This document defines every feature currently consumed by the AI modules from the existing CSV flat files.

## 1. incidents.csv
| Feature | Type | Consuming AIs | Required | Transformation Needed |
| :--- | :--- | :--- | :--- | :--- |
| `incident_id` | str (uuid) | Resource | Yes | Join key for resources |
| `incident_date` | str (date) | Forecast | Yes | Time-series indexing |
| `ward` | str | Ward, Flood, Forecast | Yes | Categorical grouping |
| `area` | str | Chatbot | No | Context string |
| `incident_type` | str | Ward, Forecast | Yes | Categorical grouping |
| `severity` | str | Ward | Yes | Impact weighting |
| `affected_population`| int | Ward | Yes | Impact scoring |
| `injuries` | int | Ward | Yes | Impact scoring |
| `deaths` | int | Ward | Yes | Impact scoring |
| `financial_loss` | float | Ward | Yes | Impact scoring |
| `response_time_minutes`| int | Ward | Yes | Required for Efficiency Score |
| `resolution_time_hours`| int | Ward | No | Feature extraction |
| `status` | str | Ward | Yes | Filter active vs resolved |

## 2. weather.csv
| Feature | Type | Consuming AIs | Required | Transformation Needed |
| :--- | :--- | :--- | :--- | :--- |
| `date` | str (date) | Flood | Yes | Indexing |
| `ward` | str | Flood, Chatbot, Ward | Yes | Categorical grouping |
| `rainfall_mm` | float | Flood, Chatbot | Yes | ML Feature |
| `temperature` | float | Flood | Yes | ML Feature |
| `humidity` | int | Flood | Yes | ML Feature |
| `water_level_m` | float | Flood, Chatbot | Yes | ML Feature |
| `alert_level` | str | Flood | No | Feature Extraction |

## 3. buildings.csv
| Feature | Type | Consuming AIs | Required | Transformation Needed |
| :--- | :--- | :--- | :--- | :--- |
| `building_id` | str (uuid) | Building, Chatbot | Yes | Primary inference key |
| `building_name` | str | Chatbot | Yes | Context |
| `ward` | str | Ward, Chatbot | Yes | Categorical grouping |
| `year_built` | int | Building | Yes | Actuarial age risk |
| `inspection_date` | str (date) | Building | Yes | Recency risk penalty |
| `condition` | str | Building | Yes | Actuarial base risk |
| `risk_level` | str | Building | No | Verification |

## 4. resources.csv
| Feature | Type | Consuming AIs | Required | Transformation Needed |
| :--- | :--- | :--- | :--- | :--- |
| `incident_id` | str (uuid) | Resource | Yes | Join key to incidents |
| `boats_used` | int | Resource | Yes | Equipment coefficient |
| `vehicles_used` | int | Resource | Yes | Equipment coefficient |
| `pumps_used` | int | Resource | Yes | Equipment coefficient |
| `equipment_used`| list(str) | Resource | No | Detailed tracing |

## 5. preparedness.csv
| Feature | Type | Consuming AIs | Required | Transformation Needed |
| :--- | :--- | :--- | :--- | :--- |
| `ward` | str | Ward | Yes | Categorical grouping |
| `program_type` | str | Ward | Yes | Preparedness penalty |
| `participants` | int | Ward | Yes | Preparedness volume |

## 6. teams.csv
Currently not utilized actively in ML training loops, but schema exists for future routing logic.
