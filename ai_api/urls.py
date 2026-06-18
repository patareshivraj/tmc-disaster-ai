from django.urls import path
from .views import (
    FloodPredictionView,
    WardRiskView,
    ResourceRecommendationView,
    BuildingAdvisorView,
    IncidentForecastView,
    RecommendationEngineView,
    ChatbotView,
    CopilotView,
    FirePredictionView
)

urlpatterns = [
    path('flood-prediction/', FloodPredictionView.as_view(), name='api-flood-prediction'),
    path('fire-prediction/', FirePredictionView.as_view(), name='api-fire-prediction'),
    path('ward-risk/<str:ward>/', WardRiskView.as_view(), name='api-ward-risk'),
    path('resource-recommendation/', ResourceRecommendationView.as_view(), name='api-resource-recommendation'),
    path('building-advisor/', BuildingAdvisorView.as_view(), name='api-building-advisor'),
    path('forecast/', IncidentForecastView.as_view(), name='api-forecast'),
    path('recommendations/', RecommendationEngineView.as_view(), name='api-recommendations'),
    path('chatbot/', ChatbotView.as_view(), name='api-chatbot'),
    path('copilot/', CopilotView.as_view(), name='api-copilot'),
]
