import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_project.settings')
django.setup()

from ai_engine.copilot.copilot_engine import CopilotEngine
from ai_engine.copilot.prompt_builder import build_messages

engine = CopilotEngine()
history = engine._get_session_history("legacy_chatbot_session")
messages = build_messages(history, "total incidents")
import json
print(json.dumps(messages, indent=2))
