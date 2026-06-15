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

def monitor_request(module_name):
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            start_time = time.time()
            res = func(self, request, *args, **kwargs)
            end_time = time.time()
            duration_ms = (end_time - start_time) * 1000
            
            # Extract input properly
            input_payload = request.data if request.data else kwargs
            output_payload = res.data if status.is_success(res.status_code) else None
            error_message = str(res.data) if status.is_client_error(res.status_code) or status.is_server_error(res.status_code) else None
            log_status = 'SUCCESS' if status.is_success(res.status_code) else 'ERROR'
            
            if module_name == 'Chatbot AI' and log_status == 'SUCCESS':
                LoggingService.log_chatbot(
                    question=input_payload.get('question', ''),
                    intent=output_payload.get('intent', 'Unknown'),
                    modules_used=output_payload.get('modules_used', []),
                    answer=output_payload.get('answer', ''),
                    confidence=output_payload.get('confidence', 0),
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
            try:
                result = ai_service.get_flood_prediction(serializer.validated_data)
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResourceRecommendationView(APIView):
    permission_classes = [AllowAny]
    @monitor_request('Resource AI')
    def post(self, request):
        serializer = ResourceRecommendationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                result = ai_service.get_resource_recommendation(serializer.validated_data)
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IncidentForecastView(APIView):
    permission_classes = [AllowAny]
    @monitor_request('Forecast AI')
    def post(self, request):
        serializer = IncidentForecastSerializer(data=request.data)
        if serializer.is_valid():
            try:
                result = ai_service.get_forecast(serializer.validated_data)
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecommendationEngineView(APIView):
    permission_classes = [AllowAny]
    @monitor_request('Recommendation AI')
    def post(self, request):
        serializer = RecommendationEngineSerializer(data=request.data)
        if serializer.is_valid():
            try:
                result = ai_service.get_recommendation(serializer.validated_data)
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatbotView(APIView):
    permission_classes = [AllowAny]
    @monitor_request('Chatbot AI')
    def post(self, request):
        serializer = ChatbotSerializer(data=request.data)
        if serializer.is_valid():
            try:
                result = ai_service.process_chat_query(serializer.validated_data)
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
