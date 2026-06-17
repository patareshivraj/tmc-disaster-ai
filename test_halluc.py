import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_project.settings')
django.setup()

from ai_engine.copilot.copilot_engine import CopilotEngine

engine = CopilotEngine()

print(engine.process_query("halluc_test_1", "What should I do in an earthquake?"))
print(engine.process_query("halluc_test_2", "Explain how a tsunami works."))
