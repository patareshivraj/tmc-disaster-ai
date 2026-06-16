# PHASE 7 — REGRESSION TEST PLAN

To ensure the repository layer is mathematically flawless, the following assertions must pass before production deployment.

## The A/B Test Wrapper
A test script `tests/test_database_regression.py` will be created. It will execute the following logic:

```python
def test_flood_ai_parity():
    # 1. Run with CSV
    settings.AI_USE_LIVE_DATABASE = False
    csv_result = flood_api.predict("Majiwada-Manpada")
    
    # 2. Run with Database
    settings.AI_USE_LIVE_DATABASE = True
    db_result = flood_api.predict("Majiwada-Manpada")
    
    # 3. Assert exact mathematical equivalence
    assert csv_result['flood_probability'] == db_result['flood_probability']
    assert csv_result['confidence'] == db_result['confidence']
```

## Coverage Required
1. `test_flood_ai_parity()`
2. `test_ward_risk_parity()`
3. `test_resource_parity()`
4. `test_building_parity()`
5. `test_forecast_parity()`
6. `test_chatbot_parity()`

If any assertion fails, the Repository layer's SQL logic is flawed and must be corrected. The AI math must never be altered to "make the test pass."
