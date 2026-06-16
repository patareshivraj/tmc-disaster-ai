# PHASE 3 — FEATURE PARITY ANALYSIS

This report compares `generated_data/*.csv` against the MySQL `tmc2` tables.

## 1. Schema Drift (Column Names & Types)
* **`response_time_minutes` & `resolution_time_hours`**: The AI expects these as explicit columns in the CSV. The DB holds `reported_time`, `response_started_time`, and `resolved_time`. This is a critical drift; the repository must compute `TIMEDIFF` in minutes/hours dynamically.
* **`financial_loss` vs `estimated_loss_amount`**: The DB uses a different naming convention.
* **`affected_population` vs `affected_people`**: Naming drift.
* **`building_id` (UUID string) vs `id` (BigInt)**: The API accepts UUIDs, but the database uses auto-incrementing integers. This will break the `BuildingAdvisor` API if not handled.

## 2. Categorical Drift
* **Wards**: The CSV uses raw string names (`"Majiwada-Manpada"`). The DB uses `ward_id`, which maps to `dmd_ward.name`.
* **Incident Types**: The CSV uses strings (`"Fire"`, `"Building Collapse"`). The DB uses `disaster_category_id` mapping to `dmd_disaster_category`.

## 3. Data Structure Drift (The Resource Gap)
The CSV `resources.csv` defines resource usage per incident as a single row (`boats_used`, `vehicles_used`, `pumps_used`). 
The DB utilizes `dmd_resource_usage` linked to `dmd_equipment` or `dmd_vehicle`. This many-to-many relationship means the AI's flat CSV format must be recreated using SQL aggregations (e.g., `SUM(quantity) WHERE equipment_type = 'Pump' GROUP BY incident_id`).

**Conclusion**: Massive Structural Drift. The data exists, but the *shape* is completely incompatible with the pandas logic.
