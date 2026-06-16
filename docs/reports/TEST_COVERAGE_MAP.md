# TEST COVERAGE MAP

**Date:** June 16, 2026
**Objective:** Map all testing scenarios and scripts to their designated directory.

| Test File | Location | Subsystem Tested | Purpose |
| :--- | :--- | :--- | :--- |
| `test_api.py` | `tests/api/` | API Layer | Validates HTTP status codes and JSON payload contracts. |
| `audit_stress_test.py` | `tests/api/` | API Layer | Performs concurrency and extreme payload stress tests. |
| `test_database_regression.py` | `tests/database/` | Database Repository Layer | Validates schema extraction parity (Rows, Count, Nulls). |
| `test_live_validation.py` | `tests/integration/` | AI Models & Database | Validates mathematical equality (0.0% drift) of AI outputs between CSV and DB data. |
| `test_scenarios.py` | `tests/integration/` | Apex Engines | Simulates multi-variable disaster scenarios across the full API stack. |
| `test_monitoring.py` | `tests/monitoring/` | Monitoring Layer | Validates UUID generation, latency tracking, and database logging integrity. |
