# PHASE 1 — DATABASE DISCOVERY REPORT

## 1. Database Connection Configuration
* **Engine:** MySQL (`django.db.backends.mysql`)
* **Host:** `192.168.0.253`
* **Port:** `3306`
* **Database Name:** `tmc2`

## 2. Existing Django Models
The local `disaster` app in this AI repository contains **no local models** (`disaster/models.py` is empty). All AI logs are correctly configured in `ai_monitoring/models.py` and have been migrated successfully (`ai_monitoring_aipredictionlog`, `ai_monitoring_chatbotlog`).

## 3. Discovered Remote Tables
The live database contains an existing monolithic schema:
* `dmd_incident`
* `dmd_weather_history`
* `dmd_building`
* `dmd_building_inspection`
* `dmd_equipment`
* `dmd_resource_usage`
* `dmd_response_team`
* `dmd_ward`
* `dmd_area`
* `dmd_disaster_category`

## 4. Table Mappings
| Domain | Corresponding Database Table(s) |
| :--- | :--- |
| **Incidents** | `dmd_incident`, `dmd_disaster_category`, `dmd_ward` |
| **Weather** | `dmd_weather_history`, `dmd_ward` |
| **Buildings** | `dmd_building`, `dmd_building_inspection`, `dmd_ward` |
| **Resources** | `dmd_equipment`, `dmd_resource_usage` |
| **Preparedness** | `dmd_mock_drill` |
| **Teams** | `dmd_response_team` |

## 5. Key Discoveries
The primary architectural pattern in the database is the use of **Foreign Keys (BigInt)** for relations like `ward_id`, `area_id`, and `disaster_category_id`, whereas the current AI ecosystem relies entirely on **denormalized string values** (e.g., `"Majiwada-Manpada"`).
