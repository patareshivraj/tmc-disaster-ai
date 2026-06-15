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
from ai_monitoring.analytics import AnalyticsService
from ai_monitoring.audit import AuditTrailEngine
from ai_monitoring.models import AIPredictionLog, ChatbotLog

factory = RequestFactory()

def run_tests():
    print("Clearing old logs...")
    AIPredictionLog.objects.all().delete()
    ChatbotLog.objects.all().delete()
    
    print("Simulating API Traffic...")
    
    # 1. Flood
    req = factory.post('/api/ai/flood-prediction/', {
        "ward": "Mumbra", "rainfall": 180, "humidity": 92,
        "water_level": 2.5, "temperature": 30, "previous_flood_count": 2, "is_monsoon": 1
    }, content_type='application/json')
    FloodPredictionView.as_view()(req)
    
    # 2. Ward
    req = factory.get('/api/ai/ward-risk/Diva/')
    WardRiskView.as_view()(req, ward="Diva")
    
    # 3. Resource
    req = factory.post('/api/ai/resource-recommendation/', {
        "ward": "Diva", "flood_probability": 90.0, "risk_score": 95.0, "risk_factors": []
    }, content_type='application/json')
    ResourceRecommendationView.as_view()(req)
    
    # 4. Building
    req = factory.post('/api/ai/building-advisor/', {
        "building_id": "1762ac42-383f-4054-92c4-cde99951bd08"
    }, content_type='application/json')
    BuildingAdvisorView.as_view()(req)
    
    # 5. Forecast
    req = factory.post('/api/ai/forecast/', {
        "days": 7
    }, content_type='application/json')
    IncidentForecastView.as_view()(req)
    
    # 6. Recommendation
    req = factory.post('/api/ai/recommendations/', {
        "ward": "Diva", "flood_probability": 90.0, "ward_risk_score": 95.0,
        "resource_shortage_score": 80.0, "building_risk_score": 60.0,
        "forecast_incidents": 40.0, "forecast_severity_critical_pct": 30.0
    }, content_type='application/json')
    RecommendationEngineView.as_view()(req)
    
    # 7. Chatbot
    req = factory.post('/api/ai/chatbot/', {
        "question": "Which ward requires immediate attention?"
    }, content_type='application/json')
    ChatbotView.as_view()(req)
    
    # 8. Error Case (Flood missing field)
    req = factory.post('/api/ai/flood-prediction/', {
        "ward": "Mumbra", "rainfall": 180
    }, content_type='application/json')
    FloodPredictionView.as_view()(req)
    
    print("--- Analytics Output ---")
    analytics = AnalyticsService.get_dashboard_metrics()
    print(json.dumps(analytics, indent=2, default=str))

    print("\n--- Audit Trail Test ---")
    log = AIPredictionLog.objects.first()
    print("Fetched Log:", log.module_name, "| Status:", log.status)
    audit = AuditTrailEngine.get_prediction_audit(log.prediction_id)
    print(json.dumps(audit, indent=2, default=str))
    
    clog = ChatbotLog.objects.first()
    print("\nFetched Chatbot Log:", clog.question, "| Status:", clog.status)

if __name__ == '__main__':
    run_tests()
