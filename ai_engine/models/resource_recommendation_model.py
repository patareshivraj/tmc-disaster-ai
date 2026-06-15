import joblib
import os
from ai_engine.models.ward_risk_model import WardRiskEngine

class ResourceRecommendationEngine:
    """
    Consumes outputs from Ward Risk AI and Flood Prediction AI to output actionable logistics.
    """
    def __init__(self, model_path='ai_engine/saved_models/resource_recommendation.pkl'):
        if os.path.exists(model_path):
            self.model_data = joblib.load(model_path)
            self.baselines = self.model_data['ward_baselines']
            self.allocation_rules = self.model_data['allocation_rules']
            self.weights = self.model_data['weights']
        else:
            self.model_data = None
            
        # We need the ward risk engine to calculate priorities of other wards dynamically
        self.ward_risk_engine = WardRiskEngine()

    def get_priority_rank(self, target_ward, target_demand_score):
        """Calculates dynamic priority rank by comparing to other wards' baseline risks."""
        wards = list(self.baselines.keys())
        scores = []
        for w in wards:
            if w == target_ward:
                scores.append((w, target_demand_score))
            else:
                # Get baseline risk score, assume 0 flood prob for comparison
                risk = self.ward_risk_engine.predict_ward_risk(w)['risk_score']
                demand = (0.0 * self.weights['flood_prob_weight']) + (risk * self.weights['risk_score_weight'])
                scores.append((w, demand))
                
        # Sort descending
        scores.sort(key=lambda x: x[1], reverse=True)
        for rank, (w, score) in enumerate(scores):
            if w == target_ward:
                return rank + 1
        return 1

    def recommend_resources(self, ward, flood_probability, risk_score, risk_factors):
        if not self.model_data:
            raise ValueError("Resource model not built. Run train_resource_model.py first.")
            
        if ward not in self.baselines:
            # Graceful fallback for unknown wards
            ward = "Naupada-Kopri"

        # 1. Resource Demand Engine
        demand_score = (flood_probability * self.weights['flood_prob_weight']) + (risk_score * self.weights['risk_score_weight'])
        demand_score = max(0.0, min(100.0, demand_score))
        
        # 2. Priority Engine
        priority_rank = self.get_priority_rank(ward, demand_score)
        
        # 3. Allocation & Gap Engine
        resources_needed = []
        recommendations = []
        
        # Flood Allocations
        if flood_probability >= 80:
            alloc = self.allocation_rules["Critical Flood"]
            resources_needed.append({"resource": "Water Pumps", "quantity": alloc["Water Pumps"], "reason": f"Critical flood risk ({flood_probability}%) combined with resource shortage."})
            resources_needed.append({"resource": "Rescue Boats", "quantity": alloc["Rescue Boats"], "reason": "High probability of severe waterlogging requiring evacuation."})
            recommendations.append("Deploy Additional Pumps")
            recommendations.append("Increase Rescue Capacity")
        elif flood_probability >= 40:
            alloc = self.allocation_rules["High Flood"]
            resources_needed.append({"resource": "Water Pumps", "quantity": alloc["Water Pumps"], "reason": f"High flood probability ({flood_probability}%) requires preventative pumping."})
            resources_needed.append({"resource": "Rescue Boats", "quantity": alloc["Rescue Boats"], "reason": "Pre-position boats for potential waterlogging."})
            recommendations.append("Deploy Preventative Pumps")
            
        # Building Risk Allocations
        if "High Building Risk" in risk_factors:
            alloc = self.allocation_rules["High Building Risk"]
            resources_needed.append({"resource": "Structural Response Teams", "quantity": alloc["Structural Response Teams"], "reason": "Critical structural deterioration detected in ward."})
            recommendations.append("Deploy Structural Response Teams")
            
        # General Risk
        if risk_score > 60:
            alloc = self.allocation_rules["High Generic Risk"]
            resources_needed.append({"resource": "Emergency Vehicles", "quantity": alloc["Emergency Vehicles"], "reason": f"Ward risk score ({risk_score}) indicates high baseline emergency probability."})
            resources_needed.append({"resource": "Rescue Teams", "quantity": alloc["Rescue Teams"], "reason": "General high vulnerability threshold crossed."})
            recommendations.append("Pre-position Emergency Teams")
            
        # If no strict triggers hit, base allocation
        if not resources_needed:
            resources_needed.append({"resource": "Emergency Vehicles", "quantity": 1, "reason": "Standard operational readiness."})
            recommendations.append("Maintain Standard Vigilance")

        return {
            "ward": ward,
            "priority_rank": priority_rank,
            "resource_demand_score": float(round(demand_score, 2)),
            "resources_needed": resources_needed,
            "recommendations": recommendations
        }
