import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_project.settings')
django.setup()

from django.conf import settings
print(f"API KEY IN SETTINGS: {getattr(settings, 'OPENAI_API_KEY', 'NOT_FOUND')}")
print(f"API KEY IN ENV: {os.environ.get('OPENAI_API_KEY')}")
