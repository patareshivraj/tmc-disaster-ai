from ai_engine.chatbot.intent_engine import IntentEngine
ie = IntentEngine()
queries = [
    'Who is the mayor of Mars?',
    'What is the capital of France?',
    'Tell me a joke',
    'What is 2+2?',
    'Which ward requires immediate attention?',
    'deploy pumps',
    'Where should I focus resources today?',
]
for q in queries:
    r = ie.detect_intent(q)
    print(f"Q: {q}")
    print(f"   intent={r['primary_intent']}, sim={r['similarity_score']}")
    print()
