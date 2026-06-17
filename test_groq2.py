import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_project.settings')
django.setup()

from ai_engine.copilot.copilot_engine import CopilotEngine
from ai_engine.copilot.prompt_builder import build_messages
engine = CopilotEngine()

import json
messages = [{"role": "system", "content": "You are a test."}, {"role": "user", "content": "total incidents"}]
try:
    print("Sending...")
    res = engine.llm.generate(messages, tools=engine.router.get_tools())
    print("Success:", res)
except Exception as e:
    print("FAILED:", type(e).__name__, str(e))
