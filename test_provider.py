import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_project.settings')
django.setup()

from ai_engine.llm.openai_provider import OpenAIProvider

provider = OpenAIProvider()
print("KEY:", provider.api_key)
print("MODEL:", provider.model)
