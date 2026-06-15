from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta
from .models import AIPredictionLog, ChatbotLog

class AnalyticsService:
    @staticmethod
    def get_dashboard_metrics():
        now = timezone.now()
        yesterday = now - timedelta(days=1)
        last_week = now - timedelta(days=7)
        
        return {
            "daily_usage": AIPredictionLog.objects.filter(timestamp__gte=yesterday).count() + ChatbotLog.objects.filter(timestamp__gte=yesterday).count(),
            "weekly_usage": AIPredictionLog.objects.filter(timestamp__gte=last_week).count() + ChatbotLog.objects.filter(timestamp__gte=last_week).count(),
            "module_distribution": list(AIPredictionLog.objects.values('module_name').annotate(count=Count('module_name')).order_by('-count')),
            "average_response_times": list(AIPredictionLog.objects.values('module_name').annotate(avg_time=Avg('response_time_ms'))),
            "chatbot_response_time": ChatbotLog.objects.aggregate(Avg('response_time_ms'))['response_time_ms__avg'],
            "error_rate": AIPredictionLog.objects.filter(status='ERROR').count() / max(1, AIPredictionLog.objects.count()) * 100
        }
