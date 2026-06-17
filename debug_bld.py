import sys
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_project.settings')
django.setup()

from ai_engine.copilot.copilot_engine import CopilotEngine
engine = CopilotEngine()
try:
    print(engine.router.orchestrator.building_ai.buildings_df)
except Exception as e:
    print("NO:", e)
