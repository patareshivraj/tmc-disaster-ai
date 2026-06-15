import sys
import os

# Ensure the parent modules can be loaded
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from ai_engine.models.ward_risk_model import WardRiskEngine
from ai_engine.models.resource_recommendation_model import ResourceRecommendationEngine
from ai_engine.models.building_advisor_model import BuildingAdvisorEngine
from ai_engine.models.incident_forecast_model import IncidentForecastEngine
from ai_engine.models.recommendation_engine import RecommendationEngine
from ai_engine.models.flood_model import FloodPredictionEngine

class ChatbotOrchestrator:
    """
    Routes the structured intent to the appropriate underlying AI models.
    """
    def __init__(self):
        try:
            self.ward_ai = WardRiskEngine()
            self.resource_ai = ResourceRecommendationEngine()
            self.building_ai = BuildingAdvisorEngine()
            self.forecast_ai = IncidentForecastEngine()
            self.rec_ai = RecommendationEngine()
            self.flood_ai = FloodPredictionEngine()
        except Exception as e:
            print(f"Warning: Model load failure in Orchestrator - {e}")
            self.ward_ai = None
            
        self.wards = ["Diva", "Kalwa", "Mumbra", "Wagle Estate", "Naupada-Kopri", "Majiwada-Manpada", "Vartak Nagar", "Uthalsar", "Lokmanya-Savarkar Nagar"]

    def _get_ward_payload(self, ward):
        """Synthesizes the unified data contract for the Recommendation Engine."""
        w_res = self.ward_ai.predict_ward_risk(ward)
        f_res = self.flood_ai.predict_flood_risk(ward, 120, 85, 3.2, 28, 2, 1) # Mock current weather context
        r_res = self.resource_ai.recommend_resources(ward, f_res["flood_probability"], w_res["risk_score"], w_res["risk_factors"])
        forecast_res = self.forecast_ai.forecast_incidents(7)
        
        shortage_score = 0.0
        for r in r_res["resources_needed"]:
            shortage_score += r.get("shortage", 0)
        shortage_score = min(100.0, shortage_score * 10)
        
        return {
            "ward": ward,
            "flood_probability": f_res["flood_probability"],
            "ward_risk_score": w_res["risk_score"],
            "resource_shortage_score": shortage_score,
            "building_risk_score": 50.0, # Defaulting building risk for general queries
            "forecast_incidents": forecast_res["expected_incidents"],
            "forecast_severity_critical_pct": forecast_res["severity_distribution"].get("Critical", 0.0)
        }

    def execute(self, parsed_intent):
        intent = parsed_intent["primary_intent"]
        ward = parsed_intent["target_ward"]
        
        results = {}
        
        try:
            if intent == "Unknown":
                results["error"] = "Query is outside the scope of disaster management intelligence."
                results["modules_used"] = []
                
            elif intent == "City-Wide" or (intent in ["Emergency", "Recommendation"] and not ward):
                # Run full city evaluation
                payloads = [self._get_ward_payload(w) for w in self.wards]
                city_eval = self.rec_ai.evaluate_city(payloads)
                
                # Get the top critical ward details
                top_ward = list(city_eval.keys())[0]
                top_payload = next(p for p in payloads if p["ward"] == top_ward)
                top_rec = self.rec_ai.generate_recommendations(top_payload)
                
                results["city_summary"] = city_eval
                results["top_ward_details"] = top_rec
                results["forecast"] = self.forecast_ai.forecast_incidents(7)
                results["modules_used"] = ["Flood Prediction AI", "Ward Risk AI", "Resource AI", "Forecast AI", "Recommendation AI"]
                
            elif intent in ["Emergency", "Recommendation", "Ward Risk"]:
                if not ward: ward = "Diva" # Fallback
                payload = self._get_ward_payload(ward)
                results["recommendation"] = self.rec_ai.generate_recommendations(payload)
                results["modules_used"] = ["Flood Prediction AI", "Ward Risk AI", "Forecast AI", "Recommendation AI"]
                
            elif intent == "Forecast":
                results["forecast"] = self.forecast_ai.forecast_incidents(30)
                results["modules_used"] = ["Forecast AI"]
                
            elif intent == "Resource":
                if not ward: ward = "Diva"
                payload = self._get_ward_payload(ward)
                r_res = self.resource_ai.recommend_resources(ward, payload["flood_probability"], payload["ward_risk_score"], [])
                results["resource"] = r_res
                results["recommendation"] = self.rec_ai.generate_recommendations(payload)
                results["modules_used"] = ["Resource AI", "Recommendation AI"]
                
            elif intent == "Building":
                import pandas as pd
                b_df = pd.read_csv("generated_data/buildings.csv")
                b_id = b_df.iloc[0]['building_id']
                b_res = self.building_ai.predict_building_risk(b_id)
                results["building"] = b_res
                results["modules_used"] = ["Building Advisor AI"]
                
            elif intent == "Flood":
                if not ward: ward = "Diva"
                f_res = self.flood_ai.predict_flood_risk(ward, 120, 85, 3.2, 28, 2, 1)
                results["flood"] = f_res
                results["modules_used"] = ["Flood Prediction AI"]
                
            else:
                # General fallback
                payloads = [self._get_ward_payload(w) for w in self.wards[:3]]
                results["city_summary"] = self.rec_ai.evaluate_city(payloads)
                results["modules_used"] = ["Recommendation AI", "Ward Risk AI"]

        except Exception as e:
            results["error"] = str(e)
            if "modules_used" not in results:
                results["modules_used"] = []
            
        return results
