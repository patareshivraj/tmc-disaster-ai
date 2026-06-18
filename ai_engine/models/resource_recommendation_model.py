import pickle
import joblib
import os
import math
from ai_engine.models.ward_risk_model import WardRiskEngine

class ResourceRecommendationEngine:
    """
    Data-Driven Hybrid AI Engine for Resource Allocation and Gap Analysis.
    """
    def __init__(self, model_path=None):
        if model_path is None:
            import os
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(base_dir, 'saved_models', 'resource_recommendation.pkl')
        if os.path.exists(model_path):
            try:
                self.model_data = joblib.load(model_path)
            except (FileNotFoundError, EOFError, pickle.UnpicklingError, Exception) as e:
                from ai_monitoring.services import LoggingService
                LoggingService.log_prediction(
                    module_name=self.__class__.__name__,
                    request_source='SYSTEM',
                    input_payload={},
                    output_payload=None,
                    confidence=0,
                    response_time=0,
                    status='ERROR',
                    error_message=f"Model loading failed: {str(e)}",
                    endpoint='STARTUP'
                )
                from ai_engine.exceptions import AIUnavailableException
                raise AIUnavailableException("AI model unavailable")
            self.baselines = self.model_data['ward_baselines']
            self.usage_coefficients = self.model_data['usage_coefficients']
            self.weights = self.model_data['weights']
        else:
            self.model_data = None
            
        self.ward_risk_engine = WardRiskEngine()

    def get_priority_rank(self, target_ward, target_demand_score):
        """Calculates dynamic priority rank."""
        wards = list(self.baselines.keys())
        scores = []
        for w in wards:
            if w == target_ward:
                scores.append((w, target_demand_score))
            else:
                risk = self.ward_risk_engine.predict_ward_risk(w)['risk_score']
                demand = risk # Scale competing ward's score dynamically based on pure risk to ensure fair ranking
                scores.append((w, demand))
                
        scores.sort(key=lambda x: x[1], reverse=True)
        for rank, (w, score) in enumerate(scores):
            if w == target_ward:
                return rank + 1
        return 1

    def recommend_resources(self, ward, flood_probability, risk_score, risk_factors, current_inventory=None):
        if not self.model_data:
            raise ValueError("Resource model not built. Run train_resource_model.py first.")
            
        if ward not in self.baselines:
            ward = "Naupada-Kopri"
            
        if current_inventory is None:
            current_inventory = {}

        # 0. Ward-Specific Historical Baselines
        # Each ward has its own learned historical resource usage profile from the live DB.
        # We compute a per-ward scaling factor relative to the global average.
        ward_baseline = self.baselines[ward]
        all_avg_pumps = sum(b['avg_pumps_used'] for b in self.baselines.values()) / len(self.baselines)
        all_avg_boats = sum(b['avg_boats_used'] for b in self.baselines.values()) / len(self.baselines)
        all_avg_vehicles = sum(b['avg_vehicles_used'] for b in self.baselines.values()) / len(self.baselines)
        
        # Ward-specific multipliers: if a ward historically uses more resources, it scales up
        pump_scale = ward_baseline['avg_pumps_used'] / all_avg_pumps if all_avg_pumps > 0 else 1.0
        boat_scale = ward_baseline['avg_boats_used'] / all_avg_boats if all_avg_boats > 0 else 1.0
        vehicle_scale = ward_baseline['avg_vehicles_used'] / all_avg_vehicles if all_avg_vehicles > 0 else 1.0

        # 1. Data-Driven Allocation Logic (Ward-Aware)
        # Combines severity inputs with ward-specific historical scaling factors.
        severity = (flood_probability / 100.0) * (risk_score / 50.0)  # Normalized severity [0..2]
        
        required_pumps = max(1, math.ceil(ward_baseline['avg_pumps_used'] * severity * pump_scale))
        required_boats = max(0, math.ceil(ward_baseline['avg_boats_used'] * severity * boat_scale))
        required_teams = math.ceil((risk_score / 100.0) * self.usage_coefficients['team_coefficient'] * 3.0)
        required_vehicles = max(0, math.ceil(ward_baseline['avg_vehicles_used'] * severity * vehicle_scale))
        
        if "High Building Risk" in risk_factors:
            required_structural_teams = math.ceil(self.usage_coefficients['structural_coefficient'] * 2.0)
        else:
            required_structural_teams = 0

        target_allocations = {
            "Water Pumps": required_pumps,
            "Rescue Boats": required_boats,
            "Rescue Teams": required_teams,
            "Emergency Vehicles": required_vehicles,
            "Structural Response Teams": required_structural_teams
        }

        # 2. True Gap Analysis
        resources_needed = []
        recommendations = []
        total_shortage_units = 0
        total_required_units = 0
        
        for resource_type, required_qty in target_allocations.items():
            if required_qty > 0:
                available_qty = current_inventory.get(resource_type, 0)
                shortage = max(0, required_qty - available_qty)
                
                total_required_units += required_qty
                total_shortage_units += shortage
                
                if shortage > 0:
                    resources_needed.append({
                        "resource": resource_type,
                        "required": required_qty,
                        "available": available_qty,
                        "shortage": shortage,
                        "reason": f"Data-driven requirement ({required_qty}) exceeds current inventory ({available_qty})."
                    })
                    if resource_type == "Water Pumps": recommendations.append("Deploy Additional Pumps")
                    if resource_type == "Rescue Boats": recommendations.append("Reallocate Boats")
                    if resource_type == "Emergency Vehicles": recommendations.append("Increase Vehicle Coverage")
                    if resource_type == "Structural Response Teams": recommendations.append("Deploy Structural Teams")

        # Deduplicate recommendations
        recommendations = list(set(recommendations))
        if not recommendations:
            recommendations.append("Maintain Standard Vigilance")

        # 3. Shortage & Gap Scoring
        if total_required_units > 0:
            resource_gap_score = (total_shortage_units / total_required_units) * 100.0
        else:
            resource_gap_score = 0.0
            
        resource_shortage_score = min(100.0, total_shortage_units * 5.0)

        # 4. Enhanced Demand Engine
        demand_score = (
            (flood_probability * self.weights['flood_prob_weight']) + 
            (risk_score * self.weights['risk_score_weight']) + 
            (resource_gap_score * self.weights['gap_score_weight'])
        )
        demand_score = max(0.0, min(100.0, demand_score))
        
        # 5. Priority Engine
        priority_rank = self.get_priority_rank(ward, demand_score)

        return {
            "ward": ward,
            "priority_rank": priority_rank,
            "resource_demand_score": float(round(demand_score, 2)),
            "resource_gap_score": float(round(resource_gap_score, 2)),
            "resource_shortage_score": float(round(resource_shortage_score, 2)),
            "resources_needed": resources_needed,
            "recommendations": recommendations
        }
