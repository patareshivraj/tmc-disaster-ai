import sys
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_project.settings')
django.setup()

from ai_engine.copilot.copilot_engine import CopilotEngine
try:
    engine = CopilotEngine()
    res = engine.process_query("test_session", "risky building in mumbra")
    print("SUCCESS")
    print(res)
except Exception as e:
    print("ERROR:", e)
