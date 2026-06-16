# PHASE 4 — BREAKAGE RISK REPORT

If the system points directly to the Database without an abstraction layer today, the following catastrophic breakages will occur:

| Component | Risk Severity | Root Cause | Fix Strategy |
| :--- | :--- | :--- | :--- |
| **All Training Scripts (`train_*.py`)** | CRITICAL | Code calls `pd.read_csv()`. | Replace with a `Repository.get_all_as_dataframe()` method. |
| **Ward Risk API Endpoint** | CRITICAL | API payload sends string `"Naupada-Kopri"`. The DB uses `ward_id=3`. The AI feature pipeline will crash during lookup. | Repository layer must perform a lookup and translate `ward_id` back to string names before handing off to the AI. |
| **Building Advisor API Endpoint** | CRITICAL | Existing logic expects UUIDs. The DB uses `id` (BigInt). The API will return `404 Not Found` for all UUIDs. | API serializers must be updated to accept integers, or a mapping table must be created. |
| **Chatbot Intent Router** | HIGH | Hardcoded to read `weather.csv` inside `chatbot_orchestrator.py` to get historical context. | Orchestrator must call `WeatherRepository.get_historical_average_for_ward()`. |
| **Feature Engineering (`create_flood_features`)** | CRITICAL | Expects column `response_time_minutes`. Will throw `KeyError` because the DB does not have this column. | Repository SQL query must include `SELECT TIMESTAMPDIFF(MINUTE, reported_time, resolved_time) as response_time_minutes`. |

**Conclusion:** Zero AI pipelines will survive a direct database swap. An intermediary layer is mandatory.
