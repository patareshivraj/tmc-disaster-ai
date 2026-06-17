import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_project.settings')
django.setup()

from ai_engine.chatbot.intent_engine import IntentEngine
ie = IntentEngine()
res = ie.detect_intent("total incidents")
print(res)
