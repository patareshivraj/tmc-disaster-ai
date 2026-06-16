# DATABASE FEATURE MAPPING

This document dictates the SQL Transformation necessary to rebuild the AI Flat Files from the 3NF MySQL Database.

## 1. Incidents
Target: `incidents.csv` equivalent DataFrame
```sql
SELECT 
    i.id as incident_id,
    i.incident_date,
    w.name as ward,
    a.name as area,
    c.name as incident_type,
    i.severity,
    i.affected_people as affected_population,
    i.injured_people as injuries,
    i.death_count as deaths,
    i.estimated_loss_amount as financial_loss,
    TIMESTAMPDIFF(MINUTE, i.reported_time, i.response_started_time) as response_time_minutes,
    TIMESTAMPDIFF(HOUR, i.reported_time, i.resolved_time) as resolution_time_hours,
    i.status
FROM dmd_incident i
JOIN dmd_ward w ON i.ward_id = w.id
JOIN dmd_area a ON i.area_id = a.id
JOIN dmd_disaster_category c ON i.disaster_category_id = c.id
```

## 2. Weather
Target: `weather.csv` equivalent DataFrame
```sql
SELECT 
    w.date,
    wd.name as ward,
    w.rainfall_mm,
    w.temperature,
    w.humidity,
    w.water_level_m,
    w.alert_level
FROM dmd_weather_history w
JOIN dmd_ward wd ON w.ward_id = wd.id
```

## 3. Buildings
Target: `buildings.csv` equivalent DataFrame
```sql
SELECT 
    b.id as building_id,
    b.name as building_name,
    w.name as ward,
    a.name as area,
    b.year_built,
    (SELECT MAX(inspection_date) FROM dmd_building_inspection bi WHERE bi.building_id = b.id) as inspection_date,
    b.condition,
    b.risk_level,
    'Audit Needed' as recommended_action
FROM dmd_building b
JOIN dmd_ward w ON b.ward_id = w.id
JOIN dmd_area a ON b.area_id = a.id
```

## 4. Resources
Target: `resources.csv` equivalent DataFrame
```sql
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
```
*(Note: Mock columns injected to satisfy legacy DataContracts where DB schema cannot map directly)*

## 5. Preparedness
Target: `preparedness.csv` equivalent DataFrame
```sql
SELECT 
    md.id as program_id,
    w.name as ward,
    md.drill_type as program_type,
    md.date,
    md.participants,
    'Successful' as outcome
FROM dmd_mock_drill md
JOIN dmd_ward w ON md.ward_id = w.id
```
