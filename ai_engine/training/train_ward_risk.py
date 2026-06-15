import os
import json
import joblib
import pandas as pd

def train_and_save_hybrid_model():
    print("Computing baseline risk factors from historical data...")
    
    # Load historical datasets
    incidents = pd.read_csv("generated_data/incidents.csv")
    buildings = pd.read_csv("generated_data/buildings.csv")
    preparedness = pd.read_csv("generated_data/preparedness.csv")
    
    wards = [
        "Naupada-Kopri", "Uthalsar", "Wagle Estate", "Lokmanya-Savarkar Nagar",
        "Vartak Nagar", "Majiwada-Manpada", "Kalwa", "Mumbra", "Diva"
    ]
    
    ward_baselines = {}
    
    for ward in wards:
        # Incident Frequency
        ward_incidents = incidents[incidents['ward'] == ward]
        incident_count = len(ward_incidents)
        severe_count = len(ward_incidents[ward_incidents['severity'].isin(['Major', 'Critical'])])
        
        # Flood Count
        flood_count = len(ward_incidents[ward_incidents['incident_type'].isin(['Flood', 'Water Logging'])])
        
        # Fire Count
        fire_count = len(ward_incidents[ward_incidents['incident_type'] == 'Fire'])
        
        # Building Risk (Weight C1 heavily)
        ward_buildings = buildings[buildings['ward'] == ward]
        c1_count = len(ward_buildings[ward_buildings['risk_level'] == 'C1'])
        c2a_count = len(ward_buildings[ward_buildings['risk_level'] == 'C2A'])
        building_risk_score = (c1_count * 3) + (c2a_count * 2)
        
        # Preparedness Score
        ward_prep = preparedness[preparedness['ward'] == ward]
        prep_score = len(ward_prep) * 1.5  # Simple placeholder
        
        # Response Efficiency (Average response time)
        avg_response_time = ward_incidents['response_time_minutes'].mean()
        if pd.isna(avg_response_time):
            avg_response_time = 30.0
            
        ward_baselines[ward] = {
            "incident_count": incident_count,
            "severe_ratio": severe_count / max(incident_count, 1),
            "flood_count": flood_count,
            "fire_count": fire_count,
            "building_risk_score": building_risk_score,
            "preparedness_score": prep_score,
            "avg_response_time": float(avg_response_time)
        }
        
    # Calculate Min-Max for normalization across wards
    metrics_to_scale = ["incident_count", "flood_count", "building_risk_score", "preparedness_score", "avg_response_time"]
    scalers = {}
    
    for metric in metrics_to_scale:
        vals = [w[metric] for w in ward_baselines.values()]
        scalers[metric] = {
            "min": min(vals),
            "max": max(vals)
        }
        
    hybrid_model = {
        "ward_baselines": ward_baselines,
        "scalers": scalers,
        "weights": {
            "flood_risk": 0.35,
            "incident_frequency": 0.20,
            "building_risk": 0.20,
            "preparedness_penalty": -0.10, # Good preparedness reduces risk
            "response_efficiency": 0.15   # High response time increases risk
        }
    }
    
    # Save the hybrid scoring engine logic
    os.makedirs('ai_engine/saved_models', exist_ok=True)
    joblib.dump(hybrid_model, 'ai_engine/saved_models/ward_risk_model.pkl')
    
    # Generate and save metrics
    metrics = {
        "engine_type": "Hybrid Risk Scoring",
        "total_wards_analyzed": len(wards),
        "scaling_parameters": scalers,
        "weight_distribution": hybrid_model["weights"]
    }
    with open('ai_engine/saved_models/ward_risk_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)
    
    print("Hybrid Ward Risk Model and metrics computed and serialized successfully!")

if __name__ == "__main__":
    train_and_save_hybrid_model()
