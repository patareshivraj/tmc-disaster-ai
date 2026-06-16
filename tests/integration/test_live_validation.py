import os
import django
import pandas as pd
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_project.settings')
django.setup()

from django.conf import settings
from ai_engine.models.flood_model import FloodPredictionEngine
from ai_engine.models.ward_risk_model import WardRiskEngine
from ai_engine.models.resource_recommendation_model import ResourceRecommendationEngine
from ai_engine.models.building_advisor_model import BuildingAdvisorEngine
from ai_engine.models.incident_forecast_model import IncidentForecastEngine
from ai_engine.chatbot.chatbot_engine import ChatbotEngine

def run_validations():
    results = {}
    
    # 1. Flood API Comparison
    print("Testing Flood AI...")
    flood_engine = FloodPredictionEngine()
    settings.AI_USE_LIVE_DATABASE = False
    csv_flood = flood_engine.predict_flood_risk("Diva", 150.0, 30.0, 80, 2.5, 0, 1)
    settings.AI_USE_LIVE_DATABASE = True
    db_flood = flood_engine.predict_flood_risk("Diva", 150.0, 30.0, 80, 2.5, 0, 1)
    results['Flood AI'] = {'CSV': csv_flood, 'DB': db_flood}

    # 2. Ward Risk Comparison
    print("Testing Ward Risk AI...")
    ward_engine = WardRiskEngine()
    settings.AI_USE_LIVE_DATABASE = False
    csv_ward = ward_engine.predict_ward_risk("Diva")
    settings.AI_USE_LIVE_DATABASE = True
    db_ward = ward_engine.predict_ward_risk("Diva")
    results['Ward Risk AI'] = {'CSV': csv_ward, 'DB': db_ward}

    # 3. Resource AI Comparison
    print("Testing Resource AI...")
    resource_engine = ResourceRecommendationEngine()
    settings.AI_USE_LIVE_DATABASE = False
    csv_res = resource_engine.recommend_resources("Diva", csv_flood['flood_probability'], csv_ward['risk_score'], csv_ward['risk_factors'])
    settings.AI_USE_LIVE_DATABASE = True
    db_res = resource_engine.recommend_resources("Diva", db_flood['flood_probability'], db_ward['risk_score'], db_ward['risk_factors'])
    results['Resource AI'] = {'CSV': csv_res, 'DB': db_res}

    # 4. Building Advisor Comparison
    print("Testing Building Advisor...")
    from ai_engine.repositories.factory import DataSourceFactory

    settings.AI_USE_LIVE_DATABASE = False
    bld_engine_csv = BuildingAdvisorEngine()
    csv_buildings = DataSourceFactory.get_dataframe("buildings")
    csv_bld_id = csv_buildings.iloc[0]['building_id']
    csv_bld = bld_engine_csv.predict_building_risk(csv_bld_id)
    
    settings.AI_USE_LIVE_DATABASE = True
    bld_engine_db = BuildingAdvisorEngine()
    db_buildings = DataSourceFactory.get_dataframe("buildings")
    db_bld_id = db_buildings.iloc[0]['building_id']
    db_bld = bld_engine_db.predict_building_risk(db_bld_id)
    results['Building AI'] = {'CSV': csv_bld, 'DB': db_bld}

    # 5. Forecast AI Comparison
    print("Testing Forecast AI...")
    forecast_engine = IncidentForecastEngine()
    settings.AI_USE_LIVE_DATABASE = False
    csv_for = forecast_engine.forecast_incidents(7)
    settings.AI_USE_LIVE_DATABASE = True
    db_for = forecast_engine.forecast_incidents(7)
    results['Forecast AI'] = {'CSV': csv_for, 'DB': db_for}

    # 6. Chatbot Comparison
    print("Testing Chatbot...")
    chatbot = ChatbotEngine()
    q = "What is the situation in Diva?"
    settings.AI_USE_LIVE_DATABASE = False
    csv_chat = chatbot.answer_question(q)
    settings.AI_USE_LIVE_DATABASE = True
    chatbot = ChatbotEngine() # re-init
    db_chat = chatbot.answer_question(q)
    results['Chatbot'] = {'CSV': csv_chat, 'DB': db_chat}
    
    with open('validation_results.json', 'w') as f:
        json.dump(results, f, indent=4)
        
    print("Validation run complete. Check validation_results.json")

if __name__ == "__main__":
    run_validations()
