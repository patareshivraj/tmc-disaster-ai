import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_project.settings')
django.setup()

from ai_api.services import AIServiceLayer
service = AIServiceLayer()
res = service.process_chat_query({"question": "total incidents"})
print(res)
