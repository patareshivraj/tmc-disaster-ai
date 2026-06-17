import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_project.settings')
django.setup()

from ai_engine.copilot.copilot_engine import CopilotEngine
from ai_engine.copilot.prompt_builder import build_messages
engine = CopilotEngine()

messages = build_messages([], "total incidents")
try:
    from openai import OpenAI
    client = OpenAI(api_key=engine.llm.api_key, base_url="https://api.groq.com/openai/v1")
    res = client.chat.completions.create(model=engine.llm.model, messages=messages, tools=engine.router.get_tools())
    print("Success")
except Exception as e:
    if hasattr(e, 'response'):
        print(e.response.json())
    elif hasattr(e, 'body'):
        print(e.body)
    else:
        print(e)
