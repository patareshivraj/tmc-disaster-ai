import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_project.settings')
django.setup()

from ai_engine.copilot.copilot_engine import CopilotEngine
engine = CopilotEngine()

import json
try:
    res = engine.process_query("test", "total incidents")
    print(json.dumps(res, indent=2))
except Exception as e:
    import traceback
    traceback.print_exc()
