import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_project.settings')
django.setup()

from django.core.cache import cache
hist = cache.get("copilot_session_legacy_chatbot_session")
print(hist)
