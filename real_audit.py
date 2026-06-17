import sys
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_project.settings')
django.setup()

from ai_engine.copilot.copilot_engine import CopilotEngine

def print_result(title, result):
    print(f"\n{'='*50}\n{title}\n{'='*50}")
    print(f"Answer: {result.get('answer', '')}")
    print(f"Tools Used: {result.get('tools_used', [])}")
    print(f"Token Usage: {result.get('token_usage', 0)}")
    print(f"Confidence: {result.get('confidence', 0)}")
    print(f"Error: {result.get('error', '')}")

def run_audit():
    engine = CopilotEngine()
    session_id = "audit_session_1"
    
    # 1
    q1 = "Why is Diva critical?"
    r1 = engine.process_query(session_id, q1)
    print_result(f"Q: {q1}", r1)
    
    # 2
    q2 = "How many pumps should we deploy there?"
    r2 = engine.process_query(session_id, q2)
    print_result(f"Q: {q2}", r2)
    
    # 3
    session_id2 = "audit_session_2"
    q3 = "Give me today's disaster briefing."
    r3 = engine.process_query(session_id2, q3)
    print_result(f"Q: {q3}", r3)
    
    # 4
    session_id3 = "audit_session_3"
    q4 = "Compare Diva and Kalwa."
    r4 = engine.process_query(session_id3, q4)
    print_result(f"Q: {q4}", r4)

if __name__ == '__main__':
    run_audit()
