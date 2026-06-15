import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_project.settings')
django.setup()

from django.test import RequestFactory
from ai_api.views import (
    FloodPredictionView,
    WardRiskView,
    ResourceRecommendationView,
    BuildingAdvisorView,
    IncidentForecastView,
    RecommendationEngineView,
    ChatbotView
)

factory = RequestFactory()

def test_scenario_1():
    print("--- Scenario 1: Extreme Monsoon (Mumbra) ---")
    req = factory.post('/api/ai/flood-prediction/', {
        "ward": "Mumbra", "rainfall": 180, "humidity": 92,
        "water_level": 2.5, "temperature": 30, "previous_flood_count": 2, "is_monsoon": 1
    }, content_type='application/json')
    res = FloodPredictionView.as_view()(req)
    print("Flood API:", res.status_code)

def test_scenario_2():
    print("--- Scenario 2: Dangerous Building (Diva) ---")
    req = factory.post('/api/ai/building-advisor/', {
        "building_id": "1762ac42-383f-4054-92c4-cde99951bd08"
    }, content_type='application/json')
    res = BuildingAdvisorView.as_view()(req)
    print("Building API:", res.status_code)

def test_scenario_3():
    print("--- Scenario 3: Resource Shortage (Kalwa) ---")
    req = factory.post('/api/ai/resource-recommendation/', {
        "ward": "Kalwa", "flood_probability": 85.0, "risk_score": 90.0, "risk_factors": []
    }, content_type='application/json')
    res = ResourceRecommendationView.as_view()(req)
    print("Resource API:", res.status_code)

def test_scenario_4():
    print("--- Scenario 4: City-Wide Emergency ---")
    req = factory.post('/api/ai/chatbot/', {
        "question": "Give me city summary."
    }, content_type='application/json')
    res = ChatbotView.as_view()(req)
    print("Chatbot API:", res.status_code)

if __name__ == "__main__":
    test_scenario_1()
    test_scenario_2()
    test_scenario_3()
    test_scenario_4()
