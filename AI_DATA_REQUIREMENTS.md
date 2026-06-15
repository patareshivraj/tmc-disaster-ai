# TMC Disaster Management AI Layer — Data Contract & Requirements

This document serves as the formal AI Data Contract between the Backend Development Team and the AI Engineering Team for the Thane Municipal Corporation (TMC) Disaster Management Department. It defines the required datasets, schemas, machine learning inputs/outputs, and API contracts necessary to implement the AI Layer.

---

## 1. AI Modules Overview

### 1.1 Flood Prediction AI
*   **Purpose:** Predict the likelihood and severity of flooding in specific wards based on meteorological and historical data.
*   **Business Objective:** Enable proactive evacuations, pump deployments, and public warnings before flood events occur.
*   **Required Inputs:** Rainfall (mm), Water level (m), Ward ID, Historical flood records for the ward.
*   **Expected Outputs:** Risk Level (Low/Medium/High/Critical), Probability percentage, Recommended immediate actions.
*   **Expected Prediction Type:** Binary/Multiclass Classification (Risk Level) and Regression (Probability).
*   **Expected Recommendation Type:** Rule-based action recommendations tied to risk thresholds.
*   **Success Criteria:** >85% recall on high-risk flood events; false positive rate <20%.

### 1.2 Ward Risk Analysis AI
*   **Purpose:** Determine the overall, real-time disaster vulnerability of each TMC ward.
*   **Business Objective:** Assist HODs in allocating long-term resources and infrastructure upgrades effectively across wards.
*   **Required Inputs:** Historical incidents count, Population density, Average response times, Seasonal disaster trends.
*   **Expected Outputs:** Aggregated Risk Score (0-100), Risk Level, Primary risk factors (Reasons), Strategic Recommendations.
*   **Expected Prediction Type:** Risk Scoring Algorithm / Clustering.
*   **Expected Recommendation Type:** Strategic and infrastructural suggestions.
*   **Success Criteria:** High correlation between the generated risk score and actual incident frequency in subsequent months.

### 1.3 Resource Recommendation AI
*   **Purpose:** Recommend the exact allocation of disaster response resources based on incident characteristics.
*   **Business Objective:** Prevent resource overallocation in minor incidents and shortages in major emergencies.
*   **Required Inputs:** Incident Type, Severity Level, Ward, Historical resource usage for similar incidents.
*   **Expected Outputs:** Recommended number of Teams, Boats, Pumps, Vehicles, and specialized equipment.
*   **Expected Prediction Type:** Multi-output Regression / KNN-based historical matching.
*   **Expected Recommendation Type:** Quantitative resource allocation mapping.
*   **Success Criteria:** Recommendations match or improve upon historical expert allocations in >90% of tested past incidents.

### 1.4 Building Safety Advisor AI
*   **Purpose:** Provide data-driven recommendations on dangerous and dilapidated buildings.
*   **Business Objective:** Minimize building collapse incidents and guide the C1/C2/C3/C4 categorizations and actions.
*   **Required Inputs:** Building Age, Structural Condition, Inspection History, Ward, Current Risk Category.
*   **Expected Outputs:** Recommended Action (Monitor, Repair, Reconstruct, Evacuate, Demolish).
*   **Expected Prediction Type:** Multiclass Classification.
*   **Expected Recommendation Type:** Categorical safety protocol recommendation.
*   **Success Criteria:** Zero false negatives on "Demolish/Evacuate" classifications for buildings that historically collapsed.

### 1.5 Incident Forecast AI
*   **Purpose:** Forecast the expected volume and type of future incidents over a specific time horizon (e.g., next month/season).
*   **Business Objective:** Aid in budget planning, resource stockpiling, and preemptive preparedness programs.
*   **Required Inputs:** Historical Disaster Records (2018-2026), Seasonal Patterns, Long-term Weather Trends.
*   **Expected Outputs:** Estimated counts for Floods, Fires, Tree Falls, etc., and identification of High-Risk Wards for the period.
*   **Expected Prediction Type:** Time Series Forecasting (ARIMA, Prophet, or LSTM).
*   **Expected Recommendation Type:** Preemptive alert flagging.
*   **Success Criteria:** Forecasted incident counts fall within a ±15% Mean Absolute Percentage Error (MAPE) margin.

### 1.6 Disaster Management Chatbot
*   **Purpose:** Allow disaster management officers to naturally query the database and AI predictions using conversational language.
*   **Business Objective:** Reduce time-to-insight during critical emergencies without requiring complex dashboard navigation.
*   **Required Inputs:** Natural Language User Query, Contextual Database Access (Read-Only).
*   **Expected Outputs:** Natural language response, structured data tables, or direct AI module execution results.
*   **Expected Prediction Type:** Large Language Model (LLM) intent classification and Retrieval-Augmented Generation (RAG).
*   **Expected Recommendation Type:** Context-aware actionable insights.
*   **Success Criteria:** Accurately parses >95% of standard officer intents (e.g., "Show me flood risk in Kalwa").

---

## 2. Required Datasets

### 2.1 Incident History Dataset
*   **Purpose:** Core training data for risk analysis, forecasting, and resource recommendations.
*   **Description:** A comprehensive log of all reported disaster incidents from 2018-2026 across all 9 TMC wards.
*   **Primary Key:** `incident_id`
*   **Relationships:** 
    *   1-to-Many with `Resource Usage History`
    *   Implicit Many-to-1 with `Weather History` (via `ward` and `incident_date`)
*   **Fields, Data Types & Sample Values:**
    *   `incident_id` (UUID): e.g., "550e8400-e29b-41d4-a716-446655440000"
    *   `incident_date` (DateTime): e.g., "2023-07-15T14:30:00Z"
    *   `incident_year` (Integer): e.g., 2023
    *   `incident_month` (Integer): e.g., 7
    *   `ward` (String): e.g., "Naupada-Kopri", "Mumbra"
    *   `area` (String): e.g., "Kharegaon"
    *   `incident_type` (String): e.g., "Flood", "Fire", "Tree Fall"
    *   `incident_category` (String): e.g., "Natural", "Structural"
    *   `cause` (String): e.g., "Heavy Rainfall", "Short Circuit"
    *   `severity` (String): e.g., "Minor", "Major", "Critical"
    *   `affected_population` (Integer): e.g., 450
    *   `injuries` (Integer): e.g., 5
    *   `deaths` (Integer): e.g., 0
    *   `financial_loss` (Decimal): e.g., 500000.00
    *   `response_time` (Integer): e.g., 45 (minutes)
    *   `resolution_time` (Integer): e.g., 24 (hours)
    *   `status` (String): e.g., "Resolved", "Ongoing"

### 2.2 Weather History Dataset
*   **Purpose:** Establish correlation between meteorological events and disaster incidents, crucial for Flood Prediction and Forecasting.
*   **Description:** Daily meteorological recordings per ward.
*   **Primary Key:** `weather_id`
*   **Relationships:** Implicit Many-to-Many with `Incident History` via temporal and spatial joints.
*   **Fields, Data Types & Sample Values:**
    *   `weather_id` (UUID): e.g., "112e8400-e29b-41d4-a716-446655440001"
    *   `date` (Date): e.g., "2023-07-15"
    *   `ward` (String): e.g., "Kalwa"
    *   `rainfall_mm` (Float): e.g., 125.5
    *   `water_level_m` (Float): e.g., 4.2
    *   `temperature` (Float): e.g., 28.5 (Celsius)
    *   `humidity` (Float): e.g., 92.0 (%)
    *   `alert_level` (String): e.g., "Yellow", "Orange", "Red"

### 2.3 Building Inspection Dataset
*   **Purpose:** Training data for the Building Safety Advisor AI.
*   **Description:** Records of structural audits and TMC categorizations (C1-C4) of buildings.
*   **Primary Key:** `building_id`
*   **Relationships:** Independent dataset; structurally relates to `ward`.
*   **Fields, Data Types & Sample Values:**
    *   `building_id` (UUID): e.g., "333e8400-e29b-41d4-a716-446655440003"
    *   `building_name` (String): e.g., "Sai Krupa CHS"
    *   `ward` (String): e.g., "Diva"
    *   `area` (String): e.g., "Diva East"
    *   `year_built` (Integer): e.g., 1985
    *   `building_age` (Integer): e.g., 41
    *   `inspection_date` (Date): e.g., "2024-03-10"
    *   `condition` (String): e.g., "Poor", "Dilapidated"
    *   `risk_level` (String): e.g., "C1", "C2A", "C3"
    *   `recommended_action` (String): e.g., "Evacuate", "Repair"

### 2.4 Resource Usage History Dataset
*   **Purpose:** Training data for Resource Recommendation AI to learn optimal deployment strategies.
*   **Description:** Records of what equipment was used during specific historical incidents.
*   **Primary Key:** `resource_id`
*   **Foreign Keys:** `incident_id` (References `Incident History`)
*   **Relationships:** Many-to-1 with `Incident History`.
*   **Fields, Data Types & Sample Values:**
    *   `resource_id` (UUID): e.g., "444e8400-e29b-41d4-a716-446655440004"
    *   `incident_id` (UUID): e.g., "550e8400-e29b-41d4-a716-446655440000"
    *   `boats_used` (Integer): e.g., 2
    *   `vehicles_used` (Integer): e.g., 3
    *   `pumps_used` (Integer): e.g., 1
    *   `equipment_used` (JSON): e.g., '["chainsaw", "ropes"]'
    *   `fuel_consumed` (Float): e.g., 45.5 (Liters)

### 2.5 Response Team Dataset
*   **Purpose:** Understand capacity and availability for Ward Risk and Resource modules.
*   **Description:** Inventory and profiling of available emergency response units.
*   **Primary Key:** `team_id`
*   **Relationships:** Independent tracking system; functionally deployed against incidents.
*   **Fields, Data Types & Sample Values:**
    *   `team_id` (UUID): e.g., "777e8400-e29b-41d4-a716-446655440007"
    *   `team_name` (String): e.g., "Alpha Rescue Team"
    *   `ward` (String): e.g., "Majiwada-Manpada"
    *   `leader_name` (String): e.g., "Rajesh Patil"
    *   `member_count` (Integer): e.g., 12
    *   `vehicles` (Integer): e.g., 2
    *   `boats` (Integer): e.g., 1
    *   `equipment_count` (Integer): e.g., 50
    *   `availability` (String): e.g., "Available", "Deployed"

### 2.6 Preparedness Program Dataset
*   **Purpose:** Evaluate if preparedness offsets risk for the Ward Risk Analysis.
*   **Description:** Records of drills, awareness campaigns, and training.
*   **Primary Key:** `program_id`
*   **Relationships:** Aggregated per `ward` for risk analysis.
*   **Fields, Data Types & Sample Values:**
    *   `program_id` (UUID): e.g., "999e8400-e29b-41d4-a716-446655440009"
    *   `ward` (String): e.g., "Vartak Nagar"
    *   `program_type` (String): e.g., "Mock Drill", "Citizen Awareness"
    *   `date_conducted` (Date): e.g., "2023-05-20"
    *   `participants_count` (Integer): e.g., 150

---

## 3. Machine Learning Approaches

### 3.1 Flood Prediction AI
*   **Input Features:** `rainfall_mm`, `water_level_m`, `alert_level`, rolling averages of rainfall (last 3/7 days).
*   **Target Variables:** `Risk Level` (Classification), `Probability` (Regression).
*   **Feature Importance Assumptions:** Cumulative rainfall and current water level are the highest predictors.
*   **Future Model Suggestions:** XGBoost for classification, Random Forest for probability scoring.
*   **Possible Rule-Based Approach:** If `rainfall_mm` > 150 and `water_level_m` > danger mark -> Risk Level = Critical.

### 3.2 Ward Risk Analysis AI
*   **Input Features:** Incident frequency by ward, population impact density, historical response times, weather alerts.
*   **Target Variables:** `Risk Score` (0-100).
*   **Feature Importance Assumptions:** Incident frequency carries the highest weight, followed by vulnerability (population).
*   **Future Model Suggestions:** K-Means clustering for ward grouping, Weighted Scoring algorithms.
*   **Possible Rule-Based Approach:** (Incident Count * 0.5) + (Average Severity * 0.3) + (Weather Alert * 0.2) mapped to a 0-100 scale.

### 3.3 Resource Recommendation AI
*   **Input Features:** `incident_type`, `severity`, `ward`.
*   **Target Variables:** `boats_used`, `vehicles_used`, `pumps_used`.
*   **Feature Importance Assumptions:** `incident_type` and `severity` strictly dictate resource needs.
*   **Future Model Suggestions:** Multi-output regression (LightGBM) or K-Nearest Neighbors (KNN) to find historically similar incidents.
*   **Possible Rule-Based Approach:** Static matrix (e.g., Severity=Critical, Type=Flood -> 3 Boats, 2 Pumps).

### 3.4 Building Safety Advisor AI
*   **Input Features:** `building_age`, `condition` (encoded), previous `risk_level`.
*   **Target Variables:** `recommended_action`.
*   **Feature Importance Assumptions:** `condition` and `building_age` > 30 years are strong indicators for Evacuate/Demolish.
*   **Future Model Suggestions:** Support Vector Machines (SVM) or Logistic Regression for transparent decision boundaries.
*   **Possible Rule-Based Approach:** If `risk_level` == 'C1' -> Recommend 'Evacuate and Demolish'.

### 3.5 Incident Forecast AI
*   **Input Features:** `incident_date`, `incident_type`, `ward`, seasonal indicators (month).
*   **Target Variables:** Projected counts of incidents for the next `t` periods.
*   **Feature Importance Assumptions:** High seasonality (Monsoons yield Floods/Tree Falls; Summers yield Fires).
*   **Future Model Suggestions:** Prophet (Facebook) or SARIMA for seasonality handling.
*   **Possible Rule-Based Approach:** Assume next month's incidents = average of the same month over the last 3 years.

---

## 4. Sample Records (JSON format)

**1. Flood Incident**
```json
{
  "ward": "Diva",
  "incident_type": "Flood",
  "cause": "Heavy Rainfall and High Tide",
  "severity": "Major",
  "affected_population": 450,
  "response_time": 45,
  "resolution_time": 24,
  "status": "Resolved"
}
```

**2. Fire Incident**
```json
{
  "ward": "Wagle Estate",
  "incident_type": "Fire",
  "cause": "Industrial Short Circuit",
  "severity": "Critical",
  "affected_population": 50,
  "response_time": 12,
  "resolution_time": 6,
  "status": "Resolved"
}
```

**3. Tree Fall Incident**
```json
{
  "ward": "Naupada-Kopri",
  "incident_type": "Tree Fall",
  "cause": "Strong Winds",
  "severity": "Minor",
  "affected_population": 0,
  "response_time": 20,
  "resolution_time": 2,
  "status": "Resolved"
}
```

**4. Building Emergency**
```json
{
  "ward": "Mumbra",
  "incident_type": "Building Collapse",
  "cause": "Structural Weakness (C1 category)",
  "severity": "Critical",
  "affected_population": 120,
  "response_time": 15,
  "resolution_time": 72,
  "status": "Resolved"
}
```

**5. Gas Leakage Incident**
```json
{
  "ward": "Kalwa",
  "incident_type": "Gas Leak",
  "cause": "Pipeline Rupture",
  "severity": "Major",
  "affected_population": 300,
  "response_time": 10,
  "resolution_time": 4,
  "status": "Resolved"
}
```

**6. Road Accident**
```json
{
  "ward": "Majiwada-Manpada",
  "incident_type": "Road Accident",
  "cause": "Waterlogging / Potholes",
  "severity": "Moderate",
  "affected_population": 4,
  "response_time": 15,
  "resolution_time": 3,
  "status": "Resolved"
}
```

---

## 5. Future API Contract

### POST `/api/ai/flood-prediction/`
*   **Purpose:** Request a flood risk prediction for a specific scenario.
*   **Request Payload:**
    ```json
    {
      "ward": "Kalwa",
      "rainfall_mm": 120.5,
      "water_level_m": 4.2
    }
    ```
*   **Response Payload:**
    ```json
    {
      "risk_level": "High",
      "probability": 82.5,
      "recommended_actions": ["Deploy 2 pumps", "Issue Yellow Alert"]
    }
    ```

### GET `/api/ai/ward-risk/`
*   **Purpose:** Fetch the real-time AI risk analysis for all wards.
*   **Response Payload:**
    ```json
    {
      "wards": [
        {
          "ward": "Mumbra",
          "risk_score": 78,
          "risk_level": "High",
          "reasons": ["High historical building collapses", "Dense population"],
          "recommendations": ["Conduct structural audits immediately"]
        }
      ]
    }
    ```

### POST `/api/ai/resource-recommendation/`
*   **Purpose:** Get AI recommendations for resource dispatch during a new incident.
*   **Request Payload:**
    ```json
    {
      "incident_type": "Flood",
      "severity": "Major",
      "ward": "Diva"
    }
    ```
*   **Response Payload:**
    ```json
    {
      "recommended_teams": 2,
      "recommended_boats": 3,
      "recommended_pumps": 4,
      "confidence_score": 0.92
    }
    ```

### GET `/api/ai/building-advice/`
*   **Purpose:** Fetch AI-driven safety recommendations for inspected buildings based on criteria.
*   **Request Payload (Query Params):** `?building_age=45&condition=Poor&risk_level=C2A`
*   **Response Payload:**
    ```json
    {
      "recommended_action": "Evacuate",
      "urgency": "Immediate",
      "explanation": "Age > 40 and Poor condition historically leads to 80% collapse probability in monsoon."
    }
    ```

### GET `/api/ai/forecast/`
*   **Purpose:** Retrieve the forecasted incident volume for the next 30 days.
*   **Response Payload:**
    ```json
    {
      "period": "Next 30 Days",
      "forecast": {
        "Flood": 12,
        "Tree Fall": 45,
        "Fire": 5
      },
      "high_risk_wards": ["Diva", "Kalwa", "Naupada-Kopri"]
    }
    ```

### POST `/api/ai/chat/`
*   **Purpose:** Send a natural language query to the Disaster Management Assistant.
*   **Request Payload:**
    ```json
    {
      "query": "Which ward has highest flood risk today?",
      "officer_id": "usr_9982"
    }
    ```
*   **Response Payload:**
    ```json
    {
      "response": "Based on current rainfall and water levels, Kalwa currently has the highest flood risk (High - 82%). I recommend deploying pumps proactively.",
      "data_context": {
         "ward": "Kalwa",
         "risk": "High"
      }
    }
    ```
