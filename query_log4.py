import sys
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_project.settings')
django.setup()

from ai_monitoring.models import LLMInteractionLog
logs = LLMInteractionLog.objects.order_by('-timestamp')[:5]
for log in logs:
    print(f"Status: {log.status}, Error: {log.error_message}")
