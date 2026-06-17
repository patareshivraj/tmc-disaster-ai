import sys
import os
import django
import time
import numpy as np

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_project.settings')
django.setup()

from ai_engine.copilot.copilot_engine import CopilotEngine

engine = CopilotEngine()
latencies = []
tokens = []

for i in range(10):
    start = time.time()
    res = engine.process_query(f"perf_{i}", "Why is Kalwa critical?")
    latencies.append((time.time() - start) * 1000)
    tokens.append(res.get('token_usage', 0))

print(f"P50: {np.percentile(latencies, 50):.2f} ms")
print(f"P95: {np.percentile(latencies, 95):.2f} ms")
print(f"P99: {np.percentile(latencies, 99):.2f} ms")
print(f"Avg Tokens: {np.mean(tokens):.0f}")
