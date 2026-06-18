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
from ai_engine.models.fire_model import FirePredictionEngine
from ai_engine.chatbot.chatbot_engine import ChatbotEngine

class AIServiceLayer:
    def __init__(self):
        from ai_engine.exceptions import AIUnavailableException
        try:
            self.flood_ai = FloodPredictionEngine()
        except Exception:
            self.flood_ai = None
            
        try:
            self.ward_ai = WardRiskEngine()
        except Exception:
            self.ward_ai = None
            
        try:
            self.resource_ai = ResourceRecommendationEngine()
        except Exception:
            self.resource_ai = None
            
        try:
            self.building_ai = BuildingAdvisorEngine()
        except Exception:
            self.building_ai = None
            
        try:
            self.forecast_ai = IncidentForecastEngine()
        except Exception:
            self.forecast_ai = None
            
        try:
            self.rec_ai = RecommendationEngine()
        except Exception:
            self.rec_ai = None
            
        try:
            self.fire_ai = FirePredictionEngine()
        except Exception:
            self.fire_ai = None
            
        try:
            self.chatbot_ai = ChatbotEngine()
        except Exception:
            self.chatbot_ai = None

    def get_flood_prediction(self, data):
        from ai_engine.exceptions import AIUnavailableException
        if not self.flood_ai: raise AIUnavailableException("AI model unavailable")
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
        from ai_engine.exceptions import AIUnavailableException
        if not self.ward_ai: raise AIUnavailableException("AI model unavailable")
        return self.ward_ai.predict_ward_risk(ward)

    def get_resource_recommendation(self, data):
        from ai_engine.exceptions import AIUnavailableException
        if not self.resource_ai: raise AIUnavailableException("AI model unavailable")
        
        # Pull live inventory from the MySQL Database if the caller didn't provide one
        current_inventory = data.get('current_inventory', {})
        if not current_inventory:
            from django.db import connection
            try:
                with connection.cursor() as cursor:
                    # Get real global equipment counts
                    cursor.execute("SELECT name, available_quantity FROM dmd_equipment")
                    for row in cursor.fetchall():
                        name, qty = row[0], row[1]
                        if name == 'Water Pump':
                            current_inventory['Water Pumps'] = qty
                        elif name == 'Rescue Boat':
                            current_inventory['Rescue Boats'] = qty
                        else:
                            current_inventory[name] = qty
                            
                    # Get real vehicles assigned to this specific ward
                    cursor.execute('''
                        SELECT COUNT(*) FROM dmd_vehicle v 
                        JOIN dmd_ward w ON v.ward_id = w.id 
                        WHERE w.name = %s
                    ''', [data['ward']])
                    vehicles_in_ward = cursor.fetchone()[0]
                    current_inventory['Emergency Vehicles'] = vehicles_in_ward
            except Exception as e:
                print(f"Error fetching live inventory: {e}")

        return self.resource_ai.recommend_resources(
            data['ward'], 
            data['flood_probability'], 
            data['risk_score'], 
            data['risk_factors'],
            current_inventory,
            data.get('disaster_type', 'Flood')
        )

    def get_building_risk(self, data):
        from ai_engine.exceptions import AIUnavailableException
        if not self.building_ai: raise AIUnavailableException("AI model unavailable")
        return self.building_ai.predict_building_risk(data['building_id'])

    def get_forecast(self, data):
        from ai_engine.exceptions import AIUnavailableException
        if not self.forecast_ai: raise AIUnavailableException("AI model unavailable")
        return self.forecast_ai.forecast_incidents(data['days'])

    def get_recommendation(self, data):
        from ai_engine.exceptions import AIUnavailableException
        if not self.rec_ai: raise AIUnavailableException("AI model unavailable")
        return self.rec_ai.generate_recommendations(data)

    def process_chat_query(self, data):
        # The user has explicitly requested that the Chatbot API be fully powered by the LLM (Groq)
        # to prevent hardcoded TF-IDF limitations. We bypass the deterministic engine.
        from ai_engine.copilot.copilot_engine import CopilotEngine
        engine = CopilotEngine()
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
from ai_engine.models.fire_model import FirePredictionEngine
from ai_engine.chatbot.chatbot_engine import ChatbotEngine

class AIServiceLayer:
    def __init__(self):
        from ai_engine.exceptions import AIUnavailableException
        try:
            self.flood_ai = FloodPredictionEngine()
        except Exception:
            self.flood_ai = None
            
        try:
            self.ward_ai = WardRiskEngine()
        except Exception:
            self.ward_ai = None
            
        try:
            self.resource_ai = ResourceRecommendationEngine()
        except Exception:
            self.resource_ai = None
            
        try:
            self.building_ai = BuildingAdvisorEngine()
        except Exception:
            self.building_ai = None
            
        try:
            self.forecast_ai = IncidentForecastEngine()
        except Exception:
            self.forecast_ai = None
            
        try:
            self.rec_ai = RecommendationEngine()
        except Exception:
            self.rec_ai = None
            
        try:
            self.fire_ai = FirePredictionEngine()
        except Exception:
            self.fire_ai = None
            
        try:
            self.chatbot_ai = ChatbotEngine()
        except Exception:
            self.chatbot_ai = None

    def get_flood_prediction(self, data):
        from ai_engine.exceptions import AIUnavailableException
        if not self.flood_ai: raise AIUnavailableException("AI model unavailable")
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
        from ai_engine.exceptions import AIUnavailableException
        if not self.ward_ai: raise AIUnavailableException("AI model unavailable")
        return self.ward_ai.predict_ward_risk(ward)

    def get_resource_recommendation(self, data):
        from ai_engine.exceptions import AIUnavailableException
        if not self.resource_ai: raise AIUnavailableException("AI model unavailable")
        
        # Pull live inventory from the MySQL Database if the caller didn't provide one
        current_inventory = data.get('current_inventory', {})
        if not current_inventory:
            from django.db import connection
            try:
                with connection.cursor() as cursor:
                    # Get real global equipment counts
                    cursor.execute("SELECT name, available_quantity FROM dmd_equipment")
                    for row in cursor.fetchall():
                        name, qty = row[0], row[1]
                        if name == 'Water Pump':
                            current_inventory['Water Pumps'] = qty
                        elif name == 'Rescue Boat':
                            current_inventory['Rescue Boats'] = qty
                        else:
                            current_inventory[name] = qty
                            
                    # Get real vehicles assigned to this specific ward
                    cursor.execute('''
                        SELECT COUNT(*) FROM dmd_vehicle v 
                        JOIN dmd_ward w ON v.ward_id = w.id 
                        WHERE w.name = %s
                    ''', [data['ward']])
                    vehicles_in_ward = cursor.fetchone()[0]
                    current_inventory['Emergency Vehicles'] = vehicles_in_ward
            except Exception as e:
                print(f"Error fetching live inventory: {e}")

        return self.resource_ai.recommend_resources(
            data['ward'], 
            data['flood_probability'], 
            data['risk_score'], 
            data['risk_factors'],
            current_inventory,
            data.get('disaster_type', 'Flood')
        )

    def get_building_risk(self, data):
        from ai_engine.exceptions import AIUnavailableException
        if not self.building_ai: raise AIUnavailableException("AI model unavailable")
        return self.building_ai.predict_building_risk(data['building_id'])

    def get_forecast(self, data):
        from ai_engine.exceptions import AIUnavailableException
        if not self.forecast_ai: raise AIUnavailableException("AI model unavailable")
        return self.forecast_ai.forecast_incidents(data['days'])

    def get_recommendation(self, data):
        from ai_engine.exceptions import AIUnavailableException
        if not self.rec_ai: raise AIUnavailableException("AI model unavailable")
        return self.rec_ai.generate_recommendations(data)

    def process_chat_query(self, data):
        # The user has explicitly requested that the Chatbot API be fully powered by the LLM (Groq)
        # to prevent hardcoded TF-IDF limitations. We bypass the deterministic engine.
        from ai_engine.copilot.copilot_engine import CopilotEngine
        engine = CopilotEngine()
        
        # Process query through the generative engine
        res = engine.process_query("legacy_chatbot_session", data['question'])
        
        # Format the output to match the legacy ChatbotView schema so frontend doesn't break
        return {
            "question": data['question'],
            "answer": res.get("answer", ""),
            "reasoning": res.get("tools_used", []),
            "recommended_actions": [],
            "modules_used": res.get("tools_used", []),
            "confidence": res.get("confidence", 99.0),
            "session_id": res.get("session_id", ""),
            "tools_used": res.get("tools_used", []),
            "token_usage": res.get("token_usage", 0)
        }

    def get_fire_prediction(self, data):
        from ai_engine.exceptions import AIUnavailableException
        if not self.fire_ai: raise AIUnavailableException("AI model unavailable")
        
        # Get historical fire count from DB
        historical_fire_count = 0
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT COUNT(*) FROM dmd_incident i
                    JOIN dmd_ward w ON i.ward_id = w.id
                    JOIN dmd_disaster_category c ON i.disaster_category_id = c.id
                    WHERE w.name = %s AND c.name IN ('Fire', 'Electric Hazard')
                ''', [data['ward']])
                historical_fire_count = cursor.fetchone()[0]
        except Exception as e:
            print(f"Error fetching historical fire count: {e}")
            
        return self.fire_ai.predict_fire_risk(
            ward=data['ward'],
            temperature=data['temperature'],
            humidity=data['humidity'],
            historical_fire_count=historical_fire_count
        )
