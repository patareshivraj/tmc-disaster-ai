# REPOSITORY AUDIT

**Date:** June 16, 2026
**Objective:** Comprehensive file classification for production readiness and cleanup.

| File/Folder | Category | Referenced By | Keep / Archive / Delete | Reason |
| :--- | :--- | :--- | :--- | :--- |
| `ai_engine/` | Runtime Production Code | APIs, `manage.py`, Tests | **Keep** | Core AI intelligence layer |
| `ai_api/` | Runtime Production Code | `dmd_project/urls.py`, Tests | **Keep** | Exposed REST APIs |
| `ai_monitoring/` | Runtime Production Code | `ai_api/views.py`, Django settings | **Keep** | Audit logging and performance metrics |
| `dmd_project/` | Runtime Production Code | WSGI, ASGI, Manage.py | **Keep** | Core Django config, settings, and routing |
| `disaster/` | Runtime Production Code | Django settings | **Keep** | Base Django application |
| `accounts/` | Runtime Production Code | Django settings | **Keep** | Authentication and User Management |
| `tests/` | Tests | CI/CD, Developers | **Keep** | Regression, Integration, and AI parity tests |
| `docs/` | Documentation | README, Developers | **Keep** | Architecture, Handoff, API Contracts, Audits |
| `manage.py` | Deployment Assets | Developers, WSGI | **Keep** | Django management script |
| `requirements.txt` | Deployment Assets | `pip install`, DevOps | **Keep** | Python dependency manifest |
| `.gitignore` | Deployment Assets | Git | **Keep** | Excludes compiled files and secrets |
| `.env.example` | Deployment Assets | Developers | **Keep** | Environment variable template |
| `README.md` | Documentation | External viewers | **Keep** | Root repository documentation |
| `FEATURE_PARITY_REPORT.md` | Generated Reports | Documentation Index | **Move** (to `docs/reports/`) | Audit artifact |
| `create_superuser.py` | Development Utilities | DevOps | **Move** (to `tools/maintenance/`) | Useful for bootstrapping DB |
| `master_seed.py` | Legacy Utilities | None (DB mode active) | **Move** (to `tools/maintenance/`) | Used to generate CSVs; kept for historical/testing purposes |
| `update_csv_refs.py` | Migration Utilities | None (One-time run) | **Move** (to `tools/migration/`) | Kept for auditing how the migration occurred |
