# TMC Disaster Management AI Layer — Synthetic Dataset Design

This document serves as the master blueprint for generating the synthetic, highly realistic historical datasets (2018–2026) required for the Thane Municipal Corporation (TMC) Disaster Management AI Layer. It defines schemas, distributions, generation strategies, and quality rules to ensure the data is viable for advanced machine learning model training.

---

## 1. Dataset Targets & Generation Volumes

To adequately train the 6 core AI modules, the generation strategy will target the following volumes of records over the 2018–2026 timeline across the 9 TMC wards:

*   **Incident Records:** 1,500 – 2,000 records
*   **Weather Records:** 3,000 – 5,000 records (sampled critical days / high-variance periods)
*   **Building Inspection Records:** 500 – 1,000 records
*   **Resource Usage Records:** 1,500 – 2,000 records (mapping roughly 1:1 with major incidents)
*   **Response Team Records:** 20 – 50 records
*   **Preparedness Records:** 300 – 500 records

---

## 2. Dataset Schema Designs

### 2.1 Incident Dataset
This dataset captures all emergency events to train risk, resource, and forecasting models.
*   `incident_id` (UUID): Primary Key
*   `incident_date` (DateTime): Timeline constraint 2018-2026
*   `ward` (String): Naupada-Kopri, Mumbra, Kalwa, etc.
*   `area` (String): Specific locality within the ward
*   `incident_type` (String): Flood, Water Logging, Tree Fall, Fire, Building Emergency, Road Accident, Gas Leakage, Heat Wave, Electrical Hazard, Landslide
*   `severity` (String): Minor, Moderate, Major, Critical
*   `affected_population` (Integer): Count of impacted citizens
*   `injuries` (Integer): Count of injuries
*   `deaths` (Integer): Count of fatalities
*   `financial_loss` (Decimal): Estimated property/infrastructure damage in INR
*   `response_time_minutes` (Integer): Time taken to reach site
*   `resolution_time_hours` (Integer): Total time until incident marked resolved
*   `status` (String): Resolved (almost 100% for historical), Ongoing

### 2.2 Weather Dataset
This dataset tracks meteorological conditions, featuring realistic Indian monsoon patterns (June–September).
*   `date` (Date): Timeline constraint 2018-2026
*   `ward` (String): Granular weather tracking
*   `rainfall_mm` (Float): Precipitation amount (Spikes heavily Jun-Sep)
*   `temperature` (Float): Celsius (Spikes Mar-May)
*   `humidity` (Float): Percentage
*   `water_level_m` (Float): Highest impact in creek-side wards (Kalwa, Mumbra, Diva)
*   `alert_level` (String): None, Yellow, Orange, Red

### 2.3 Building Dataset
This dataset tracks the structural integrity of infrastructure, training the Building Advisor AI.
*   `building_id` (UUID): Primary Key
*   `building_name` (String): Fictionalized society names (e.g., "Sai Krupa CHS")
*   `ward` (String): Assigned ward
*   `area` (String): Specific locality
*   `year_built` (Integer): 1950 - 2025
*   `inspection_date` (Date): Historical audit dates
*   `condition` (String): Good, Fair, Poor, Dilapidated
*   `risk_level` (String): Safe, C1, C2A, C2B, C3, C4
*   `recommended_action` (String): Monitor, Repair, Reconstruct, Evacuate, Demolish

### 2.4 Resource Usage Dataset
This dataset maps exactly what was deployed during historical incidents.
*   `resource_id` (UUID): Primary Key
*   `incident_id` (UUID): Foreign Key -> Incident Dataset
*   `boats_used` (Integer): High count for Major Floods
*   `vehicles_used` (Integer): Fire brigades, ambulances, NDRF trucks
*   `pumps_used` (Integer): High count for Water Logging
*   `equipment_used` (JSON array): e.g., ["Chainsaw", "Ropes", "Earthmover"]
*   `fuel_consumed` (Float): Liters of diesel/petrol

### 2.5 Response Team Dataset
This dataset inventories the available active rescue capacity.
*   `team_id` (UUID): Primary Key
*   `team_name` (String): e.g., "TDRF Unit 1", "Fire Brigade Mumbra"
*   `ward` (String): Stationed location
*   `leader_name` (String): Synthetic Indian names
*   `member_count` (Integer): e.g., 5-25
*   `vehicles` (Integer): Number of assigned heavy/light vehicles
*   `boats` (Integer): Number of assigned rescue boats
*   `equipment_count` (Integer): Total gears available
*   `availability` (String): Available, Deployed, Maintenance

### 2.6 Preparedness Dataset
This dataset tracks proactive municipal activities that offset risk.
*   `program_id` (UUID): Primary Key
*   `ward` (String): Target ward
*   `program_type` (String): Mock Drills, Citizen Awareness Programs, School Safety Campaigns, Hospital Preparedness Programs
*   `date` (Date): Conducted date
*   `participants` (Integer): Number of attendees
*   `outcome` (String): Successful, Needs Improvement, Excellent

---

## 3. Data Relationships

The synthetic data generation must maintain referential integrity across the following vectors:
*   **Incident → Resource Usage:** Every major/critical incident MUST have a corresponding Resource Usage record tied via `incident_id`.
*   **Ward → Weather:** Weather patterns affect specific wards. Mumbra/Kalwa/Diva will show higher `water_level_m` correlating with heavy `rainfall_mm` leading to Floods.
*   **Building → Inspection:** Inspections are evaluated against Building properties (`year_built`).
*   **Team → Incident Response:** Teams are implicitly stationed at Wards, meaning response times drop if incidents occur near high-density team stations.

---

## 4. Realistic Data Distribution

To train unbiased ML models, the `incident_type` must follow strict municipal probability distributions:

*   **Floods:** 35% (Concentrated heavily in June–September)
*   **Tree Falls:** 20% (High correlation with early monsoons and high wind speeds)
*   **Fire:** 15% (Higher correlation with summer months Mar-May, or Diwali season)
*   **Road Accidents:** 10% (Evenly distributed, slightly higher during water logging)
*   **Building Emergencies:** 8% (Highly correlated with heavy rains and old `year_built`)
*   **Gas Leakage:** 5%
*   **Heat Wave:** 3% (Strictly April/May)
*   **Electrical Hazard:** 2% (Correlated with Water Logging)
*   **Landslide:** 2% (Specific to hilly terrains like Mumbra/Parsik hill)

---

## 5. Seed Generation Strategy

To ensure data looks mathematically and logically real, the Python seed scripts will employ:

1.  **Repeatable Randomness:** Random seeds (e.g., `random.seed(42)`) will be used to ensure the generated dataset is identical across multiple environment setups.
2.  **Monsoon Season Effects:** Logic hooks will artificially skew probabilities based on the month. E.g., `if month in [6, 7, 8, 9]`, the probability of `rainfall_mm > 50` increases by 400%, which cascades to trigger Flood and Tree Fall incident generation.
3.  **Ward-Specific Patterns:**
    *   *Diva, Mumbra, Kalwa:* Higher propensity for water logging and creek-based floods.
    *   *Wagle Estate:* Higher propensity for Industrial Fires.
    *   *Naupada-Kopri:* Older infrastructure leading to Building Emergencies.
4.  **Risk Cascading:** A critical flood must automatically trigger high `boats_used` and `pumps_used` in the Resource Generation phase, ensuring the ML Resource Recommendation engine learns the correct patterns.

---

## 6. Output Design (Seed File Architecture)

The generation logic will be cleanly separated into modular scripts inside a `seeds/` directory:

*   `weather_seed.py`: Generates the baseline weather timeline. (Runs first, establishes the environmental reality).
*   `incident_seed.py`: Consumes the weather timeline. If a generated day has 200mm rainfall, it spawns floods and tree falls.
*   `building_seed.py`: Generates the static infrastructure and historical inspection logs based on age distributions.
*   `resource_seed.py`: Iterates over the output of `incident_seed.py` and assigns resources based on severity and type.
*   `team_seed.py`: Generates the static 20-50 emergency response units.
*   `preparedness_seed.py`: Generates random safety drills, skewing slightly higher in Pre-Monsoon months (April/May).
*   `master_seed.py`: The orchestrator. It imports and executes the above files in the correct chronological and dependency order to ensure foreign keys match.

---

## 7. Data Quality Rules

To prevent AI model hallucination and poor learning, the data generation must strictly adhere to:
1.  **No negative rainfall:** `rainfall_mm` must be `>= 0.0`.
2.  **No future dates:** Max date is `Current Date` or `2026-12-31`.
3.  **Logical Temporality:** `response_time_minutes` must logically fit inside `resolution_time_hours`. (You cannot resolve a flood in 1 hour if response took 90 minutes).
4.  **Resource Logic:** `boats_used` MUST be `0` for Fires. `pumps_used` MUST be `0` for Tree Falls.
5.  **Severity Logic:** Critical incidents MUST have financial loss > 0 and generally utilize more resources.
6.  **Building Logic:** A building cannot have a `year_built` after its `inspection_date`.

---

## 8. AI Training Readiness Checklist

Before moving to the ML Development phase, this generated dataset must pass the following checks:

*   [ ] **Flood Prediction:** Contains high-variance rainfall data strongly correlated with Flood/Water Logging incident timestamps.
*   [ ] **Ward Risk Analysis:** Every ward has a unique density of incidents and preparedness programs, allowing the ML clustering to successfully group high vs. low risk wards.
*   [ ] **Resource Recommendation:** Incident severity and type show a clear, learnable statistical correlation with deployed teams/vehicles/pumps.
*   [ ] **Building Advisor:** `C1/C4` risk labels strongly correlate with `Dilapidated` conditions and high `building_age`.
*   [ ] **Incident Forecast:** The 2018-2026 timeline shows clear seasonality (Prophet/ARIMA algorithms require visible cyclical patterns).
*   [ ] **Chatbot:** Data contains rich text fields (areas, causes, types) to allow the LLM to provide diverse textual responses.

*End of Design Document.*
