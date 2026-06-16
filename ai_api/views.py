import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import (
    FloodPredictionSerializer, 
    ResourceRecommendationSerializer,
    BuildingAdvisorSerializer,
    IncidentForecastSerializer,
    RecommendationEngineSerializer,
    ChatbotSerializer
)
from .services import AIServiceLayer
from ai_monitoring.services import LoggingService

ai_service = AIServiceLayer()

from ai_engine.exceptions import AIUnavailableException

def monitor_request(module_name):
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            import time
            start_time = time.time()
            try:
                res = func(self, request, *args, **kwargs)
                error_message = str(res.data) if hasattr(res, 'status_code') and status.is_client_error(res.status_code) else None
                log_status = 'SUCCESS' if hasattr(res, 'status_code') and status.is_success(res.status_code) else 'ERROR'
            except AIUnavailableException as e:
                res = Response({"status": "error", "message": "AI model unavailable"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
                error_message = str(e)
                log_status = 'ERROR'
            except Exception as e:
                res = Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                error_message = str(e)
                log_status = 'ERROR'
                
            end_time = time.time()
            duration_ms = (end_time - start_time) * 1000
            
            input_payload = request.data if hasattr(request, 'data') and request.data else kwargs
            output_payload = res.data if hasattr(res, 'status_code') and status.is_success(res.status_code) else None
            
            if module_name == 'Chatbot AI' and log_status == 'SUCCESS':
                LoggingService.log_chatbot(
                    question=input_payload.get('question', ''),
                    intent=output_payload.get('intent', 'Unknown') if output_payload else 'Unknown',
                    modules_used=output_payload.get('modules_used', []) if output_payload else [],
                    answer=output_payload.get('answer', '') if output_payload else '',
                    confidence=output_payload.get('confidence', 0) if output_payload else 0,
                    response_time=duration_ms,
                    status=log_status
                )
            else:
                conf = output_payload.get('confidence') if output_payload and isinstance(output_payload, dict) else None
                LoggingService.log_prediction(
                    module_name=module_name,
                    request_source='API',
                    input_payload=input_payload,
                    output_payload=output_payload,
                    confidence=conf,
                    response_time=duration_ms,
                    status=log_status,
                    error_message=error_message,
                    endpoint=request.path
                )
            
            return res
        return wrapper
    return decorator

class FloodPredictionView(APIView):
    permission_classes = [AllowAny]
    @monitor_request('Flood Prediction AI')
    def post(self, request):
        serializer = FloodPredictionSerializer(data=request.data)
        if serializer.is_valid():
            result = ai_service.get_flood_prediction(serializer.validated_data)
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WardRiskView(APIView):
    permission_classes = [AllowAny]
    @monitor_request('Ward Risk AI')
    def get(self, request, ward):
        try:
            result = ai_service.get_ward_risk(ward)
            return Response(result, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"error": "Ward not found in operational database"}, status=status.HTTP_404_NOT_FOUND)

class ResourceRecommendationView(APIView):
    permission_classes = [AllowAny]
    @monitor_request('Resource AI')
    def post(self, request):
        serializer = ResourceRecommendationSerializer(data=request.data)
        if serializer.is_valid():
            result = ai_service.get_resource_recommendation(serializer.validated_data)
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BuildingAdvisorView(APIView):
    permission_classes = [AllowAny]
    @monitor_request('Building Advisor AI')
    def post(self, request):
        serializer = BuildingAdvisorSerializer(data=request.data)
        if serializer.is_valid():
            try:
                result = ai_service.get_building_risk(serializer.validated_data)
                return Response(result, status=status.HTTP_200_OK)
            except IndexError:
                return Response({"error": "Building ID not found in survey dataset."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IncidentForecastView(APIView):
    permission_classes = [AllowAny]
    @monitor_request('Forecast AI')
    def post(self, request):
        serializer = IncidentForecastSerializer(data=request.data)
        if serializer.is_valid():
            result = ai_service.get_forecast(serializer.validated_data)
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecommendationEngineView(APIView):
    permission_classes = [AllowAny]
    @monitor_request('Recommendation AI')
    def post(self, request):
        serializer = RecommendationEngineSerializer(data=request.data)
        if serializer.is_valid():
            result = ai_service.get_recommendation(serializer.validated_data)
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatbotView(APIView):
    permission_classes = [AllowAny]
    @monitor_request('Chatbot AI')
    def post(self, request):
        serializer = ChatbotSerializer(data=request.data)
        if serializer.is_valid():
            result = ai_service.process_chat_query(serializer.validated_data)
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
