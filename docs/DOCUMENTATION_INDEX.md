# DOCUMENTATION INDEX

**Date:** June 16, 2026

This directory serves as the centralized repository for all project documentation.

## Architecture (`docs/architecture/`)
* `AI_API_ARCHITECTURE.md` - Schema and flow for the RESTful APIs.
* `AI_DATA_REQUIREMENTS.md` - Raw inputs needed across models.
* `AI_MONITORING_ARCHITECTURE.md` - Observability and audit logging topology.
* `AI_SYSTEM_ARCHITECTURE.md` - Global multi-agent model design.
* `CHATBOT_ARCHITECTURE.md` - NLP orchestrator flowchart and fallback logic.
* `DATA_ACCESS_ARCHITECTURE.md` - The abstraction logic for live database connectivity.
* `DATABASE_FEATURE_MAPPING.md` - SQL-to-Pandas feature transformations.
* `FEATURE_CONTRACTS.md` - Strict typing rules for model inputs.
* `REPOSITORY_LAYER_DESIGN.md` - Object-Oriented design of the data access layer.

## Audits (`docs/audits/`)
* `BREAKAGE_RISK_REPORT.md` - Analyzed risks before migrating DB logic.
* `DATA_COMPATIBILITY_AUDIT.md` - Found differences between CSV formats and DB tables.
* `DATABASE_DISCOVERY_REPORT.md` - Enumerated the live production schema tables.
* `INDEPENDENT_AUDIT_REMEDIATION_REPORT.md` - Final checklist of fixes from Phase 15.1.
* `INDEPENDENT_AUDIT_REPORT.md` - The original technical critique.
* `PHASE6_AUDIT_REPORT.md` to `PHASE8_REAUDIT_REPORT.md` - Legacy phase audits.
* `REPOSITORY_AUDIT.md` - Final codebase cleanup audit.

## Reports (`docs/reports/`)
* `DATABASE_MIGRATION_COMPLETION_REPORT.md` - Sign-off for Database integration.
* `LIVE_DATABASE_VALIDATION_REPORT.md` - Validation of zero prediction drift.
* `FEATURE_PARITY_REPORT.md` - Analysis of data availability in DB.
* `PROJECT_COMPLETION_REPORT.md` - Original phase completion sign-off.
* `TEST_COVERAGE_MAP.md` - Index of the `tests/` directory coverage.

## Handoff (`docs/handoff/`)
* `API_INTEGRATION_HANDOFF.md` - Single source of truth for UI/UX and Frontend teams.

## Root Document
* `project_timeline.md` - Engineering history from Phase 0 to Phase 15.3.
