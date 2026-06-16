# PHASE 6 — REPOSITORY LAYER DESIGN

The `ai_engine/repositories/` directory will contain Data Access Objects (DAOs) that implement a standard interface.

## 1. Interface Definition
```python
class BaseRepository:
    def __init__(self, use_db=True):
        self.use_db = use_db
        
    def get_dataframe(self) -> pd.DataFrame:
        if self.use_db:
            return self._fetch_from_db()
        return self._fetch_from_csv()
```

## 2. Core Repositories to Build

1. `IncidentRepository`
   * **SQL Goal:** `SELECT i.*, w.name as ward, c.name as incident_type, TIMESTAMPDIFF(MINUTE, i.reported_time, i.resolved_time) as response_time_minutes FROM dmd_incident i JOIN dmd_ward w ON i.ward_id = w.id JOIN dmd_disaster_category c ON i.disaster_category_id = c.id`
   * **Output:** Recreates `incidents.csv`.

2. `WeatherRepository`
   * **SQL Goal:** `SELECT w.date, wd.name as ward, w.rainfall_mm, w.temperature, w.humidity, w.water_level_m FROM dmd_weather_history w JOIN dmd_ward wd ON w.ward_id = wd.id`
   * **Output:** Recreates `weather.csv`.

3. `BuildingRepository`
   * **SQL Goal:** `SELECT b.id as building_id, b.name as building_name, w.name as ward, b.year_built, b.condition FROM dmd_building b JOIN dmd_ward w ON b.ward_id = w.id`
   * **Output:** Recreates `buildings.csv`.

4. `ResourceRepository`
   * **SQL Goal:** Complex aggregation across `dmd_equipment` and `dmd_resource_usage` grouped by incident.
   * **Output:** Recreates `resources.csv`.

## 3. Configuration Flag
The system will use a setting in `dmd_project/settings.py`:
`AI_USE_LIVE_DATABASE = True`

This single flag will switch the entire ecosystem seamlessly.
