import sys
import os

# Ensure we can load AI engine modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_engine.models.flood_model import FloodPredictionEngine
from ai_engine.models.ward_risk_model import WardRiskEngine
from ai_engine.models.resource_recommendation_model import ResourceRecommendationEngine
from ai_engine.models.building_advisor_model import BuildingAdvisorEngine
from ai_engine.models.incident_forecast_model import IncidentForecastEngine
from ai_engine.models.recommendation_engine import RecommendationEngine
from ai_engine.chatbot.chatbot_engine import ChatbotEngine

class AIServiceLayer:
    def __init__(self):
        try:
            self.flood_ai = FloodPredictionEngine()
            self.ward_ai = WardRiskEngine()
            self.resource_ai = ResourceRecommendationEngine()
            self.building_ai = BuildingAdvisorEngine()
            self.forecast_ai = IncidentForecastEngine()
            self.rec_ai = RecommendationEngine()
            self.chatbot_ai = ChatbotEngine()
        except Exception as e:
            print(f"Error loading AI engines: {e}")

    def get_flood_prediction(self, data):
        return self.flood_ai.predict_flood_risk(
            data['ward'], 
            data['rainfall'], 
            data['humidity'], 
            data['water_level'], 
            data['temperature'], 
            data['previous_flood_count'], 
            data['is_monsoon']
        )

    def get_ward_risk(self, ward):
        return self.ward_ai.predict_ward_risk(ward)

    def get_resource_recommendation(self, data):
        return self.resource_ai.recommend_resources(
            data['ward'], 
            data['flood_probability'], 
            data['risk_score'], 
            data['risk_factors']
        )

    def get_building_risk(self, data):
        return self.building_ai.predict_building_risk(data['building_id'])

    def get_forecast(self, data):
        return self.forecast_ai.forecast_incidents(data['days'])

    def get_recommendation(self, data):
        return self.rec_ai.generate_recommendations(data)

    def process_chat_query(self, data):
        return self.chatbot_ai.answer_question(data['question'])
