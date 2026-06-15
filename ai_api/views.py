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

# Initialize the service layer globally to load models once
ai_service = AIServiceLayer()

class FloodPredictionView(APIView):
    permission_classes = [AllowAny]
    
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

    def post(self, request):
        serializer = ChatbotSerializer(data=request.data)
        if serializer.is_valid():
            try:
                result = ai_service.process_chat_query(serializer.validated_data)
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
