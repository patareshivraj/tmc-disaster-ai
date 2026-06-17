import sys
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_project.settings')
django.setup()

from ai_engine.copilot.copilot_engine import CopilotEngine

def print_result(title, result):
    print(f"\n{'='*50}\n{title}\n{'='*50}")
    print(f"Answer: {result.get('answer', '')}")
    print(f"Tools Used: {result.get('tools_used', [])}")

engine = CopilotEngine()
session_id = "hallucination_session"

print_result("Q: Who is the mayor of Mars?", engine.process_query(session_id, "Who is the mayor of Mars?"))
print_result("Q: How many aliens attacked Diva?", engine.process_query(session_id, "How many aliens attacked Diva?"))
print_result("Q: Predict earthquakes next month.", engine.process_query(session_id, "Predict earthquakes next month."))
print_result("Q: Give me flood probability for a ward not present in database.", engine.process_query(session_id, "Give me flood probability for Asgard ward."))
