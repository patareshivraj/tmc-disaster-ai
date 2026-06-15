import joblib
import os

class WardRiskEngine:
    """
    Explainable Hybrid Scoring Engine for Ward Vulnerability.
    """
    def __init__(self, model_path='ai_engine/saved_models/ward_risk_model.pkl'):
        if os.path.exists(model_path):
            self.model_data = joblib.load(model_path)
            self.baselines = self.model_data['ward_baselines']
            self.scalers = self.model_data['scalers']
            self.weights = self.model_data['weights']
        else:
            self.model_data = None

    def _normalize(self, val, metric):
        min_v = self.scalers[metric]['min']
        max_v = self.scalers[metric]['max']
        if max_v == min_v:
            return 0.5
        return (val - min_v) / (max_v - min_v)

    def predict_ward_risk(self, ward):
        if not self.model_data:
            raise ValueError("Ward Risk model not built. Run train_ward_risk.py first.")
            
        if ward not in self.baselines:
            raise ValueError(f"Ward {ward} not found in historical baselines.")
            
        data = self.baselines[ward]
        
        # Calculate individual normalized risk factors (0.0 to 1.0)
        flood_factor = self._normalize(data['flood_count'], 'flood_count')
        incident_factor = self._normalize(data['incident_count'], 'incident_count')
        building_factor = self._normalize(data['building_risk_score'], 'building_risk_score')
        prep_factor = self._normalize(data['preparedness_score'], 'preparedness_score')
        response_factor = self._normalize(data['avg_response_time'], 'avg_response_time')
        
        # Apply weights to get a score out of 100
        raw_score = (
            (flood_factor * self.weights['flood_risk']) +
            (incident_factor * self.weights['incident_frequency']) +
            (building_factor * self.weights['building_risk']) +
            (prep_factor * self.weights['preparedness_penalty']) + 
            (response_factor * self.weights['response_efficiency'])
        )
        
        # Scale to 0-100 (Adjust for potential negative prep penalty)
        risk_score = max(0.0, min(100.0, (raw_score + 0.10) * 100))
        
        # Determine Level
        if risk_score > 75:
            risk_level = "Critical"
        elif risk_score > 50:
            risk_level = "High"
        elif risk_score > 25:
            risk_level = "Moderate"
        else:
            risk_level = "Low"
            
        # Determine Explainability (Top Risk Factors)
        factors = []
        if flood_factor > 0.6: factors.append("Frequent Flooding")
        if building_factor > 0.6: factors.append("High Building Risk")
        if response_factor > 0.6: factors.append("Slow Historical Response Time")
        if incident_factor > 0.6: factors.append("High Historical Incident Density")
        if prep_factor < 0.4: factors.append("Low Preparedness Score")
        if not factors: factors.append("General Vulnerability Threshold Reached")
            
        return {
            "ward": ward,
            "risk_score": float(round(risk_score, 2)),
            "risk_level": risk_level,
            "confidence": 91.0, # Fixed confidence for hybrid rules
            "risk_factors": factors
        }
