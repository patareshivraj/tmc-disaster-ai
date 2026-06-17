import sys
from ai_engine.repositories.factory import DataSourceFactory
import os
import pandas as pd

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
    Phase 15.1: Replaced mock weather with data-derived ward averages.
    """
    def __init__(self):
        self.ward_ai = None
        self.resource_ai = None
        self.building_ai = None
        self.forecast_ai = None
        self.rec_ai = None
        self.flood_ai = None
        
        try: self.ward_ai = WardRiskEngine()
        except Exception as e: print(f"Warning: WardRiskEngine load failure - {e}")
        
        try: self.resource_ai = ResourceRecommendationEngine()
        except Exception as e: print(f"Warning: ResourceRecommendationEngine load failure - {e}")
        
        try: self.building_ai = BuildingAdvisorEngine()
        except Exception as e: print(f"Warning: BuildingAdvisorEngine load failure - {e}")
        
        try: self.forecast_ai = IncidentForecastEngine()
        except Exception as e: print(f"Warning: IncidentForecastEngine load failure - {e}")
        
        try: self.rec_ai = RecommendationEngine()
        except Exception as e: print(f"Warning: RecommendationEngine load failure - {e}")
        
        try: self.flood_ai = FloodPredictionEngine()
        except Exception as e: print(f"Warning: FloodPredictionEngine load failure - {e}")

        self.wards = ["Diva", "Kalwa", "Mumbra", "Wagle Estate", "Naupada-Kopri",
                       "Majiwada-Manpada", "Vartak Nagar", "Uthalsar", "Lokmanya-Savarkar Nagar"]

        # ============================================================
        # DATA-DERIVED WEATHER CONTEXT (Phase 15.1 Mock Elimination)
        # ============================================================
        # Instead of hardcoded (120, 85, 3.2, 28, 2, 1) for all wards,
        # compute per-ward historical averages from weather.csv
        self.ward_weather = {}
        try:
            weather_df = DataSourceFactory.get_dataframe("weather")
            for ward in self.wards:
                w_data = weather_df[weather_df['ward'] == ward]
                if not w_data.empty:
                    self.ward_weather[ward] = {
                        'rainfall': float(w_data['rainfall_mm'].mean()),
                        'humidity': float(w_data['humidity'].mean()),
                        'water_level': float(w_data['water_level_m'].mean()),
                        'temperature': float(w_data['temperature'].mean()),
                    }
                else:
                    self.ward_weather[ward] = {'rainfall': 50, 'humidity': 70, 'water_level': 1.0, 'temperature': 30}
        except Exception:
            for ward in self.wards:
                self.ward_weather[ward] = {'rainfall': 50, 'humidity': 70, 'water_level': 1.0, 'temperature': 30}

        # DATA-DERIVED BUILDING RISK PER WARD (Phase 15.1 Mock Elimination)
        self.ward_building_risk = {}
        try:
            buildings_df = DataSourceFactory.get_dataframe("buildings")
            condition_map = {'Dilapidated': 90, 'Poor': 70, 'Fair': 40, 'Good': 10}
            buildings_df['risk_num'] = buildings_df['condition'].map(condition_map).fillna(50)
            for ward in self.wards:
                w_bld = buildings_df[buildings_df['ward'] == ward]
                if not w_bld.empty:
                    self.ward_building_risk[ward] = float(w_bld['risk_num'].mean())
                else:
                    self.ward_building_risk[ward] = 50.0
        except Exception:
            for ward in self.wards:
                self.ward_building_risk[ward] = 50.0

    def _get_ward_payload(self, ward):
        """Synthesizes the unified data contract using per-ward historical data."""
        if not self.ward_ai or not self.flood_ai or not self.resource_ai or not self.forecast_ai:
            from ai_engine.exceptions import AIUnavailableException
            raise AIUnavailableException("AI model unavailable")
            
        w_res = self.ward_ai.predict_ward_risk(ward)

        # Use per-ward historical weather averages instead of hardcoded mock values
        wx = self.ward_weather.get(ward, {'rainfall': 50, 'humidity': 70, 'water_level': 1.0, 'temperature': 30})
        f_res = self.flood_ai.predict_flood_risk(
            ward, wx['rainfall'], wx['humidity'], wx['water_level'], wx['temperature'], 2, 1
        )

        r_res = self.resource_ai.recommend_resources(ward, f_res["flood_probability"], w_res["risk_score"], w_res["risk_factors"])
        forecast_res = self.forecast_ai.forecast_incidents(7)

        shortage_score = 0.0
        for r in r_res["resources_needed"]:
            shortage_score += r.get("shortage", 0)
        shortage_score = min(100.0, shortage_score * 10)

        # Use per-ward computed building risk instead of hardcoded 50.0
        building_risk = self.ward_building_risk.get(ward, 50.0)

        return {
            "ward": ward,
            "flood_probability": f_res["flood_probability"],
            "ward_risk_score": w_res["risk_score"],
            "resource_shortage_score": shortage_score,
            "building_risk_score": building_risk,
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
                payloads = [self._get_ward_payload(w) for w in self.wards]
                city_eval = self.rec_ai.evaluate_city(payloads)

                top_ward = list(city_eval.keys())[0]
                top_payload = next(p for p in payloads if p["ward"] == top_ward)
                top_rec = self.rec_ai.generate_recommendations(top_payload)

                results["city_summary"] = city_eval
                results["top_ward_details"] = top_rec
                results["forecast"] = self.forecast_ai.forecast_incidents(7)
                results["modules_used"] = ["Flood Prediction AI", "Ward Risk AI", "Resource AI", "Forecast AI", "Recommendation AI"]

            elif intent in ["Emergency", "Recommendation", "Ward Risk"]:
                if not ward: ward = "Diva"
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
                if not self.building_ai:
                    from ai_engine.exceptions import AIUnavailableException
                    raise AIUnavailableException("AI model unavailable")
                b_df = DataSourceFactory.get_dataframe("buildings")
                b_id = b_df.iloc[0]['building_id']
                b_res = self.building_ai.predict_building_risk(b_id)
                results["building"] = b_res
                results["modules_used"] = ["Building Advisor AI"]

            elif intent == "Flood":
                if not ward: ward = "Diva"
                wx = self.ward_weather.get(ward, {'rainfall': 50, 'humidity': 70, 'water_level': 1.0, 'temperature': 30})
                f_res = self.flood_ai.predict_flood_risk(ward, wx['rainfall'], wx['humidity'], wx['water_level'], wx['temperature'], 2, 1)
                results["flood"] = f_res
                results["modules_used"] = ["Flood Prediction AI"]

            else:
                payloads = [self._get_ward_payload(w) for w in self.wards[:3]]
                results["city_summary"] = self.rec_ai.evaluate_city(payloads)
                results["modules_used"] = ["Recommendation AI", "Ward Risk AI"]

        except Exception as e:
            from ai_engine.exceptions import AIUnavailableException
            if isinstance(e, AIUnavailableException):
                raise
            results["error"] = str(e)
            if "modules_used" not in results:
                results["modules_used"] = []

        return results
