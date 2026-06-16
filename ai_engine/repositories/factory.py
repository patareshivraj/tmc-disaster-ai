import pandas as pd
from django.db import connection
from django.conf import settings

class BaseRepository:
    def __init__(self, csv_path):
        # Default to False if not defined in settings to prevent breakage
        self.use_db = getattr(settings, 'AI_USE_LIVE_DATABASE', False)
        self.csv_path = csv_path

    def get_dataframe(self) -> pd.DataFrame:
        if self.use_db:
            return self._fetch_from_db()
        return pd.read_csv(self.csv_path)

    def _fetch_from_db(self) -> pd.DataFrame:
        raise NotImplementedError("Subclasses must implement SQL extraction")

class IncidentRepository(BaseRepository):
    def __init__(self):
        super().__init__('generated_data/incidents.csv')

    def _fetch_from_db(self) -> pd.DataFrame:
        sql = """
        SELECT 
            i.id as incident_id,
            CAST(i.incident_date AS CHAR) as incident_date,
            w.name as ward,
            a.name as area,
            c.name as incident_type,
            i.severity,
            i.affected_people as affected_population,
            i.injured_people as injuries,
            i.death_count as deaths,
            CAST(i.estimated_loss_amount AS FLOAT) as financial_loss,
            TIMESTAMPDIFF(MINUTE, i.reported_time, i.response_started_time) as response_time_minutes,
            TIMESTAMPDIFF(HOUR, i.reported_time, i.resolved_time) as resolution_time_hours,
            i.status
        FROM dmd_incident i
        JOIN dmd_ward w ON i.ward_id = w.id
        JOIN dmd_area a ON i.area_id = a.id
        JOIN dmd_disaster_category c ON i.disaster_category_id = c.id
        """
        df = pd.read_sql(sql, connection)
        # Handle UUID cast if needed by AI modules (some expect string UUIDs)
        # The AI expects string, so we'll cast id to string.
        df['incident_id'] = df['incident_id'].astype(str)
        # response_time_minutes can be null if response hasn't started
        df['response_time_minutes'] = df['response_time_minutes'].fillna(0).astype(int)
        df['resolution_time_hours'] = df['resolution_time_hours'].fillna(0).astype(int)
        return df

class WeatherRepository(BaseRepository):
    def __init__(self):
        super().__init__('generated_data/weather.csv')

    def _fetch_from_db(self) -> pd.DataFrame:
        sql = """
        SELECT 
            CAST(w.date AS CHAR) as date,
            wd.name as ward,
            CAST(w.rainfall_mm AS FLOAT) as rainfall_mm,
            CAST(w.temperature AS FLOAT) as temperature,
            w.humidity,
            CAST(w.water_level_m AS FLOAT) as water_level_m,
            w.alert_level
        FROM dmd_weather_history w
        JOIN dmd_ward wd ON w.ward_id = wd.id
        """
        return pd.read_sql(sql, connection)

class BuildingRepository(BaseRepository):
    def __init__(self):
        super().__init__('generated_data/buildings.csv')

    def _fetch_from_db(self) -> pd.DataFrame:
        sql = """
        SELECT 
            b.id as building_id,
            b.name as building_name,
            w.name as ward,
            a.name as area,
            b.year_built,
            CAST((SELECT MAX(inspection_date) FROM dmd_building_inspection bi WHERE bi.building_id = b.id) AS CHAR) as inspection_date,
            b.condition,
            b.risk_level,
            'Audit Needed' as recommended_action
        FROM dmd_building b
        JOIN dmd_ward w ON b.ward_id = w.id
        JOIN dmd_area a ON b.area_id = a.id
        """
        df = pd.read_sql(sql, connection)
        df['building_id'] = df['building_id'].astype(str)
        # Provide default inspection date if missing
        df['inspection_date'] = df['inspection_date'].fillna('2023-01-01')
        return df

class ResourceRepository(BaseRepository):
    def __init__(self):
        super().__init__('generated_data/resources.csv')

    def _fetch_from_db(self) -> pd.DataFrame:
        sql = """
        SELECT 
            ru.incident_id as incident_id,
            MAX(ru.id) as resource_id,
            SUM(CASE WHEN e.name LIKE '%Boat%' THEN ru.quantity_used ELSE 0 END) as boats_used,
            SUM(CASE WHEN v.id IS NOT NULL THEN ru.quantity_used ELSE 0 END) as vehicles_used,
            SUM(CASE WHEN e.name LIKE '%Pump%' THEN ru.quantity_used ELSE 0 END) as pumps_used,
            '[]' as equipment_used,
            0.0 as fuel_consumed
        FROM dmd_resource_usage ru
        LEFT JOIN dmd_equipment e ON ru.equipment_id = e.id
        LEFT JOIN dmd_vehicle v ON ru.vehicle_id = v.id
        GROUP BY ru.incident_id
        """
        df = pd.read_sql(sql, connection)
        df['incident_id'] = df['incident_id'].astype(str)
        df['resource_id'] = df['resource_id'].astype(str)
        df['boats_used'] = df['boats_used'].fillna(0).astype(int)
        df['vehicles_used'] = df['vehicles_used'].fillna(0).astype(int)
        df['pumps_used'] = df['pumps_used'].fillna(0).astype(int)
        return df

class PreparednessRepository(BaseRepository):
    def __init__(self):
        super().__init__('generated_data/preparedness.csv')

    def _fetch_from_db(self) -> pd.DataFrame:
        sql = """
        SELECT 
            md.id as program_id,
            w.name as ward,
            md.drill_type as program_type,
            CAST(md.date AS CHAR) as date,
            md.participants,
            'Successful' as outcome
        FROM dmd_mock_drill md
        JOIN dmd_ward w ON md.ward_id = w.id
        """
        df = pd.read_sql(sql, connection)
        df['program_id'] = df['program_id'].astype(str)
        return df

class DataSourceFactory:
    _repositories = {
        'incidents': IncidentRepository,
        'weather': WeatherRepository,
        'buildings': BuildingRepository,
        'resources': ResourceRepository,
        'preparedness': PreparednessRepository,
    }

    @classmethod
    def get_repository(cls, name: str) -> BaseRepository:
        if name not in cls._repositories:
            raise ValueError(f"Repository {name} not found.")
        return cls._repositories[name]()

    @classmethod
    def get_dataframe(cls, name: str) -> pd.DataFrame:
        return cls.get_repository(name).get_dataframe()
