# PHASE 2 — DATA COMPATIBILITY AUDIT

All AI modules currently consume data purely from `generated_data/*.csv`. 

| Module | Current Data Source | Expected Features | Actual DB Fields | Compatibility | Missing / Extra Fields |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Flood AI** | `weather.csv` | `ward` (str), `rainfall_mm`, `temperature`, `humidity`, `water_level_m` | `ward_id` (int), `rainfall_mm`, `temperature`, `humidity`, `water_level_m` | **85%** | `ward` string is missing. Requires SQL JOIN with `dmd_ward`. |
| **Ward Risk AI** | All 5 CSVs | `incident_type`, `response_time_minutes`, `financial_loss` | `disaster_category_id`, `reported_time`, `resolved_time`, `estimated_loss_amount` | **40%** | Requires heavy computation mapping (time diffs) and multiple JOINs to resolve integer IDs to strings. |
| **Resource AI** | `resources.csv`, `incidents.csv` | `boats_used`, `vehicles_used`, `pumps_used` | Scattered across `dmd_resource_usage`, `dmd_equipment` | **20%** | Massive structural difference. Equipment usage is normalized in DB, but AI expects a flat table. |
| **Building Advisor**| `buildings.csv` | `building_id` (uuid), `year_built`, `condition`, `inspection_date` | `id` (bigint), `year_built`, `condition` | **70%** | `inspection_date` is missing from base table; requires JOIN with `dmd_building_inspection`. `id` format differs. |
| **Forecast AI** | `incidents.csv` | `incident_date`, `incident_type`, `ward` | `incident_date`, `disaster_category_id`, `ward_id` | **80%** | Foreign key resolution required. |
| **Chatbot** | `weather.csv`, `buildings.csv` | Per-ward averages grouped by string | Aggregation on DB tables required | **50%** | API strings won't match DB `ward_id`. |

**Overall Assessment:** The AI models expect heavily denormalized (flat) DataFrames. The live MySQL database is highly normalized (3NF). Direct consumption is impossible without an abstraction layer.
