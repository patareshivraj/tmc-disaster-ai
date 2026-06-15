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

def run_tests():
    print("Testing Flood API...")
    req = factory.post('/api/ai/flood-prediction/', {
        "ward": "Mumbra", "rainfall": 180, "humidity": 92,
        "water_level": 2.5, "temperature": 30, "previous_flood_count": 2, "is_monsoon": 1
    }, content_type='application/json')
    res = FloodPredictionView.as_view()(req)
    print("Flood Status:", res.status_code)

    print("Testing Ward Risk API...")
    req = factory.get('/api/ai/ward-risk/Diva/')
    res = WardRiskView.as_view()(req, ward="Diva")
    print("Ward Status:", res.status_code)

    print("Testing Resource API...")
    req = factory.post('/api/ai/resource-recommendation/', {
        "ward": "Diva", "flood_probability": 90.0, "risk_score": 95.0, "risk_factors": []
    }, content_type='application/json')
    res = ResourceRecommendationView.as_view()(req)
    print("Resource Status:", res.status_code)

    print("Testing Building API...")
    req = factory.post('/api/ai/building-advisor/', {
        "building_id": "1762ac42-383f-4054-92c4-cde99951bd08"  # fallback or real if matches
    }, content_type='application/json')
    res = BuildingAdvisorView.as_view()(req)
    print("Building Status:", res.status_code)

    print("Testing Forecast API...")
    req = factory.post('/api/ai/forecast/', {
        "days": 7
    }, content_type='application/json')
    res = IncidentForecastView.as_view()(req)
    print("Forecast Status:", res.status_code)

    print("Testing Recommendation API...")
    req = factory.post('/api/ai/recommendations/', {
        "ward": "Diva", "flood_probability": 90.0, "ward_risk_score": 95.0,
        "resource_shortage_score": 80.0, "building_risk_score": 60.0,
        "forecast_incidents": 40.0, "forecast_severity_critical_pct": 30.0
    }, content_type='application/json')
    res = RecommendationEngineView.as_view()(req)
    print("Recommendation Status:", res.status_code)

    print("Testing Chatbot API...")
    req = factory.post('/api/ai/chatbot/', {
        "question": "Which ward requires immediate attention?"
    }, content_type='application/json')
    res = ChatbotView.as_view()(req)
    print("Chatbot Status:", res.status_code)

if __name__ == '__main__':
    run_tests()
