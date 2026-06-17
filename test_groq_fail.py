import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_project.settings')
django.setup()

from ai_engine.copilot.copilot_engine import CopilotEngine
engine = CopilotEngine()
try:
    res = engine.llm.generate([{"role": "user", "content": "total incidents"}], tools=engine.router.get_tools())
    print(res)
except Exception as e:
    import traceback
    traceback.print_exc()
