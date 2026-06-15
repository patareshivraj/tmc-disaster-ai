import os, django, json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_project.settings')
django.setup()
from django.test import RequestFactory
from ai_api.views import *

factory = RequestFactory()

print('=== HARD STRESS TEST ===')
print()

# 1. Flood with IDENTICAL inputs but different wards
print('--- TEST 1: Same weather, different wards ---')
for ward in ['Mumbra', 'Diva', 'Kalwa', 'Naupada-Kopri']:
    req = factory.post('/api/ai/flood-prediction/', {
        'ward': ward, 'rainfall': 180, 'humidity': 92,
        'water_level': 2.5, 'temperature': 30, 'previous_flood_count': 2, 'is_monsoon': 1
    }, content_type='application/json')
    res = FloodPredictionView.as_view()(req)
    d = res.data
    print(f"  {ward}: prob={d['flood_probability']}, risk={d['risk_level']}, conf={d['confidence']}")

print()

# 2. Flood with LOW rainfall
print('--- TEST 2: Low rainfall should predict low ---')
req = factory.post('/api/ai/flood-prediction/', {
    'ward': 'Mumbra', 'rainfall': 5, 'humidity': 30,
    'water_level': 0.1, 'temperature': 35, 'previous_flood_count': 0, 'is_monsoon': 0
}, content_type='application/json')
res = FloodPredictionView.as_view()(req)
d = res.data
print(f"  Mumbra LOW: prob={d['flood_probability']}, risk={d['risk_level']}")

print()

# 3. Ward Risk variance test
print('--- TEST 3: Ward scores should differ ---')
scores = {}
for ward in ['Diva', 'Mumbra', 'Naupada-Kopri', 'Wagle Estate', 'Kalwa']:
    req = factory.get(f'/api/ai/ward-risk/{ward}/')
    res = WardRiskView.as_view()(req, ward=ward)
    d = res.data
    scores[ward] = d['risk_score']
    factors = d['risk_factors']
    print(f"  {ward}: score={d['risk_score']}, level={d['risk_level']}, confidence={d['confidence']}, factors={factors}")

# Check if all scores are identical (red flag)
unique_scores = set(scores.values())
print(f"  Unique scores: {len(unique_scores)} out of {len(scores)} wards")
if len(unique_scores) == 1:
    print("  *** RED FLAG: All wards return identical risk scores! ***")

print()

# 4. Chatbot semantic equivalence
print('--- TEST 4: Semantic equivalence ---')
questions = [
    'Which ward requires immediate attention?',
    'Where should I focus resources today?',
    'Which area is currently most vulnerable?'
]
answers = []
for q in questions:
    req = factory.post('/api/ai/chatbot/', {'question': q}, content_type='application/json')
    res = ChatbotView.as_view()(req)
    d = res.data
    answers.append(d.get('answer', 'N/A'))
    print(f"  Q: {q}")
    print(f"  A: {d.get('answer', 'N/A')}")
    print(f"  Modules: {d.get('modules_used', [])}")
    print()

print()

# 5. Hallucination resistance
print('--- TEST 5: Out-of-domain queries ---')
ood_questions = [
    'Who is the mayor of Mars?',
    'What is the capital of France?',
    'Tell me a joke',
    'What is 2+2?'
]
for q in ood_questions:
    req = factory.post('/api/ai/chatbot/', {'question': q}, content_type='application/json')
    res = ChatbotView.as_view()(req)
    d = res.data
    print(f"  Q: {q}")
    print(f"  A: {d.get('answer', 'N/A')}")
    print()

print()

# 6. Hardcoded confidence check
print('--- TEST 6: Confidence score analysis ---')
# Building always returns 94
req = factory.post('/api/ai/building-advisor/', {'building_id': '1762ac42-383f-4054-92c4-cde99951bd08'}, content_type='application/json')
res = BuildingAdvisorView.as_view()(req)
print(f"  Building confidence: {res.data.get('confidence')}")

# Ward always returns 91
req = factory.get('/api/ai/ward-risk/Diva/')
res = WardRiskView.as_view()(req, ward='Diva')
print(f"  Ward confidence: {res.data.get('confidence')}")

# Chatbot always returns 94
req = factory.post('/api/ai/chatbot/', {'question': 'Which ward requires immediate attention?'}, content_type='application/json')
res = ChatbotView.as_view()(req)
print(f"  Chatbot confidence: {res.data.get('confidence')}")

# Flood confidence should vary
for ward in ['Mumbra', 'Diva']:
    for rain in [10, 180]:
        req = factory.post('/api/ai/flood-prediction/', {
            'ward': ward, 'rainfall': rain, 'humidity': 50,
            'water_level': 1.0, 'temperature': 30, 'previous_flood_count': 1, 'is_monsoon': 1
        }, content_type='application/json')
        res = FloodPredictionView.as_view()(req)
        print(f"  Flood {ward} rain={rain}: confidence={res.data.get('confidence')}, prob={res.data.get('flood_probability')}")

print()

# 7. Resource API - verify it actually computes shortages
print('--- TEST 7: Resource shortage computation ---')
req = factory.post('/api/ai/resource-recommendation/', {
    'ward': 'Diva', 'flood_probability': 95.0, 'risk_score': 90.0, 'risk_factors': []
}, content_type='application/json')
res = ResourceRecommendationView.as_view()(req)
d = res.data
print(f"  Ward: {d.get('ward')}")
print(f"  Demand Score: {d.get('resource_demand_score')}")
print(f"  Gap Score: {d.get('resource_gap_score')}")
print(f"  Resources Needed: {json.dumps(d.get('resources_needed', []), indent=4)}")

print()

# 8. Recommendation API - verify combined risk varies with input
print('--- TEST 8: Recommendation sensitivity ---')
for f_prob in [10, 50, 90]:
    req = factory.post('/api/ai/recommendations/', {
        'ward': 'Diva', 'flood_probability': f_prob, 'ward_risk_score': 80.0,
        'resource_shortage_score': 60.0, 'building_risk_score': 50.0,
        'forecast_incidents': 30.0, 'forecast_severity_critical_pct': 20.0
    }, content_type='application/json')
    res = RecommendationEngineView.as_view()(req)
    d = res.data
    print(f"  flood_prob={f_prob}: combined={d.get('combined_risk_score')}, priority={d.get('priority_level')}, escalation={d.get('escalation_level')}")

print()

# 9. Forecast API - verify it uses learned seasonality
print('--- TEST 9: Forecast consistency ---')
for days in [7, 30, 90]:
    req = factory.post('/api/ai/forecast/', {'days': days}, content_type='application/json')
    res = IncidentForecastView.as_view()(req)
    d = res.data
    print(f"  {days} days: expected={d.get('expected_incidents')}, hotspots={d.get('hotspots', [])[:3]}")
    print(f"  Explanations: {d.get('explanations', [])}")

print()
print('=== STRESS TEST COMPLETE ===')
