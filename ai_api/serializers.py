from rest_framework import serializers

class FloodPredictionSerializer(serializers.Serializer):
    ward = serializers.CharField(max_length=100)
    rainfall = serializers.FloatField(min_value=0.0)
    humidity = serializers.FloatField(min_value=0.0, max_value=100.0)
    water_level = serializers.FloatField(min_value=0.0)
    temperature = serializers.FloatField()
    previous_flood_count = serializers.IntegerField(min_value=0)
    is_monsoon = serializers.IntegerField(min_value=0, max_value=1)

class ResourceRecommendationSerializer(serializers.Serializer):
    ward = serializers.CharField(max_length=100)
    flood_probability = serializers.FloatField(min_value=0.0, max_value=100.0)
    risk_score = serializers.FloatField(min_value=0.0, max_value=100.0)
    risk_factors = serializers.ListField(child=serializers.DictField(), required=False, default=list)
    current_inventory = serializers.DictField(child=serializers.IntegerField(), required=False, default=dict)

class BuildingAdvisorSerializer(serializers.Serializer):
    building_id = serializers.CharField(max_length=100)

class IncidentForecastSerializer(serializers.Serializer):
    days = serializers.IntegerField(min_value=1, max_value=365, default=7)

class RecommendationEngineSerializer(serializers.Serializer):
    ward = serializers.CharField(max_length=100)
    flood_probability = serializers.FloatField(min_value=0.0, max_value=100.0)
    ward_risk_score = serializers.FloatField(min_value=0.0, max_value=100.0)
    resource_shortage_score = serializers.FloatField(min_value=0.0, max_value=100.0)
    building_risk_score = serializers.FloatField(min_value=0.0, max_value=100.0)
    forecast_incidents = serializers.FloatField(min_value=0.0)
    forecast_severity_critical_pct = serializers.FloatField(min_value=0.0, max_value=100.0)

class ChatbotSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=500)

class CopilotSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=1000, required=True)
    session_id = serializers.CharField(max_length=100, required=False, allow_blank=True)
