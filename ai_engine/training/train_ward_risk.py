import os
from ai_engine.repositories.factory import DataSourceFactory
import json
import joblib
import pandas as pd
import numpy as np
from datetime import datetime

def train_and_save_hybrid_model():
    print("Computing baseline risk factors from historical data (Phase 15.1 Reengineered)...")

    # Load historical datasets
    incidents = DataSourceFactory.get_dataframe("incidents")
    buildings = DataSourceFactory.get_dataframe("buildings")
    preparedness = DataSourceFactory.get_dataframe("preparedness")
    weather = DataSourceFactory.get_dataframe("weather")
    resources = DataSourceFactory.get_dataframe("resources")

    resource_incidents = pd.merge(resources, incidents[['incident_id', 'ward']], on='incident_id', how='left')

    # ==========================================================
    # GEOGRAPHIC RISK PROFILE (Explicitly documented domain priors)
    # ==========================================================
    # These multipliers represent TMC's known geographic vulnerability data.
    # They are DOMAIN EXPERT PRIORS, not learned parameters.
    # Diva/Mumbra/Kalwa are historically flood-prone low-lying areas.
    # Naupada-Kopri is an elevated, well-maintained urban zone.
    # Documented as required by Phase 15.1 Independent Audit.
    geo_multipliers = {
        "Diva": 1.6,        # Low-lying, adjacent to creek
        "Mumbra": 1.3,      # Dense informal settlement, drainage issues
        "Kalwa": 1.2,       # Industrial zone, aging infrastructure
        "Naupada-Kopri": 0.4,  # Elevated, modern infrastructure
        "Wagle Estate": 0.7    # Industrial, moderate infrastructure
    }

    wards = [
        "Naupada-Kopri", "Uthalsar", "Wagle Estate", "Lokmanya-Savarkar Nagar",
        "Vartak Nagar", "Majiwada-Manpada", "Kalwa", "Mumbra", "Diva"
    ]

    ward_baselines = {}

    for ward in wards:
        ward_incidents = incidents[incidents['ward'] == ward]
        mult = geo_multipliers.get(ward, 1.0)

        incident_count = len(ward_incidents) * mult
        severe_count = len(ward_incidents[ward_incidents['severity'].isin(['Major', 'Critical'])]) * mult
        flood_count = len(ward_incidents[ward_incidents['incident_type'].isin(['Flood', 'Water Logging'])]) * mult
        fire_count = len(ward_incidents[ward_incidents['incident_type'] == 'Fire']) * mult
        avg_response_time = ward_incidents['response_time_minutes'].mean()
        if pd.isna(avg_response_time):
            avg_response_time = 30.0

        ward_buildings = buildings[buildings['ward'] == ward]
        c1_count = len(ward_buildings[ward_buildings['risk_level'] == 'C1'])
        c2a_count = len(ward_buildings[ward_buildings['risk_level'] == 'C2A'])
        building_risk_score = ((c1_count * 3) + (c2a_count * 2)) * mult

        ward_prep = preparedness[preparedness['ward'] == ward]
        prep_score = len(ward_prep) * 2.0 * (1.0 / mult)

        ward_weather = weather[weather['ward'] == ward]
        avg_rainfall = ward_weather['rainfall_mm'].mean()
        max_rainfall = ward_weather['rainfall_mm'].max()
        extreme_weather_days = len(ward_weather[ward_weather['alert_level'].isin(['Red', 'Orange'])])
        weather_severity_score = ((avg_rainfall * 0.5) + (extreme_weather_days * 2)) * mult

        ward_resources = resource_incidents[resource_incidents['ward'] == ward]
        total_pumps = ward_resources['pumps_used'].sum()
        total_boats = ward_resources['boats_used'].sum()
        resource_consumption_score = (total_pumps + (total_boats * 2)) * mult

        ward_baselines[ward] = {
            "incident_count": float(incident_count),
            "flood_count": float(flood_count),
            "fire_count": float(fire_count),
            "building_risk_score": float(building_risk_score),
            "preparedness_score": float(prep_score),
            "avg_response_time": float(avg_response_time),
            "weather_severity_score": float(weather_severity_score),
            "resource_consumption_score": float(resource_consumption_score)
        }

    # ==========================================================
    # DATA-DERIVED WEIGHTS (Phase 15.1 Root Cause Fix)
    # ==========================================================
    # Instead of manually assigning weights, we compute the Coefficient
    # of Variation (CV = std/mean) for each feature across all wards.
    # Features with higher variance relative to their mean are more
    # discriminating between wards and should receive higher weight.
    # ==========================================================
    risk_features = ['incident_count', 'flood_count', 'building_risk_score',
                     'avg_response_time', 'weather_severity_score', 'resource_consumption_score']
    protective_features = ['preparedness_score']

    feature_cv = {}
    for feat in risk_features + protective_features:
        values = np.array([ward_baselines[w][feat] for w in ward_baselines])
        mean_val = np.mean(values)
        std_val = np.std(values)
        cv = std_val / mean_val if mean_val > 0 else 0.0
        feature_cv[feat] = cv

    # Normalize risk feature CVs to sum to 1.0
    total_risk_cv = sum(feature_cv[f] for f in risk_features)
    total_prot_cv = sum(feature_cv[f] for f in protective_features)

    weight_mapping = {
        'weather_severity_score': 'weather_severity',
        'flood_count': 'flood_risk',
        'incident_count': 'incident_frequency',
        'building_risk_score': 'building_risk',
        'resource_consumption_score': 'resource_shortage',
        'avg_response_time': 'response_efficiency',
        'preparedness_score': 'preparedness_penalty'
    }

    derived_weights = {}
    for feat in risk_features:
        w = feature_cv[feat] / total_risk_cv if total_risk_cv > 0 else 1.0 / len(risk_features)
        derived_weights[weight_mapping[feat]] = round(w, 4)

    for feat in protective_features:
        derived_weights[weight_mapping[feat]] = -round(feature_cv[feat] / total_risk_cv if total_risk_cv > 0 else 0.15, 4)

    print(f"Data-Derived Weights: {json.dumps(derived_weights, indent=2)}")
    print(f"Feature CVs: {json.dumps({k: round(v, 4) for k, v in feature_cv.items()}, indent=2)}")

    # Scale variables
    metrics_to_scale = list(set(risk_features + protective_features))
    scalers = {}
    for metric in metrics_to_scale:
        vals = [w[metric] for w in ward_baselines.values()]
        scalers[metric] = {"min": float(min(vals)), "max": float(max(vals))}

    hybrid_model = {
        "ward_baselines": ward_baselines,
        "scalers": scalers,
        "weights": derived_weights,
        "feature_cv": {k: round(v, 4) for k, v in feature_cv.items()},
        "weight_derivation_method": "Coefficient of Variation (CV = std/mean) across wards"
    }

    os.makedirs('ai_engine/saved_models', exist_ok=True)
    joblib.dump(hybrid_model, 'ai_engine/saved_models/ward_risk_model.pkl')

    metrics = {
        "version": "2.0 (Phase 15.1 Reengineered)",
        "last_training_timestamp": datetime.now().isoformat(),
        "engine_type": "Data-Derived Hybrid Risk Scoring",
        "weight_derivation": "Coefficient of Variation across ward feature distributions",
        "total_wards_analyzed": len(wards),
        "derived_weights": derived_weights,
        "feature_coefficients_of_variation": {k: round(v, 4) for k, v in feature_cv.items()},
        "scaling_parameters": scalers,
        "geographic_priors_applied": True,
        "geographic_priors_documentation": "TMC domain expert knowledge: Diva/Mumbra/Kalwa are low-lying flood-prone zones"
    }
    with open('ai_engine/saved_models/ward_risk_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)

    print("Data-Derived Ward Risk Model computed and serialized successfully!")

if __name__ == "__main__":
    train_and_save_hybrid_model()
