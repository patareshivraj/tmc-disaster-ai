# Copilot Capabilities Matrix

| Capability | Description | Status | Implementation Method |
|------------|-------------|--------|-----------------------|
| Q&A Navigation | Route queries to deterministic models | ✅ Native | `ToolRouter` intent matching |
| Multi-Tool Reasoning | Sequentially execute tools for complex tasks | ✅ Supported | `while` loop implementation up to 5 iterations |
| Evidence-Based Synthesis | Citing specific modules and numerical values | ✅ Supported | `SYSTEM_PROMPT` rules |
| Entity Resolution | Remembering context (e.g., "there" -> "Diva") | ✅ Supported | `cache` memory injected into `messages` |
| Explainability Mode | Breaking down 'Why' scenarios transparently | ✅ Supported | `SYSTEM_PROMPT` constraint on reasoning exposure |
| Operational Briefings | Executive summary spanning wards and resources | ✅ Supported | Multiple parallel tool invocations + Formatting constraint |
| Comparative Analysis | Table-based analysis across different locations | ✅ Supported | Multiple invocations + Formatting constraint |
| Uncertainty Disclosure | Suppressing deterministic hallucinated language | ✅ Supported | `SYSTEM_PROMPT` keyword restrictions ("estimates") |
| Hallucination Guardrails | Fallback for missing/unverified data | ✅ Supported | `SYSTEM_PROMPT` refusal constraint + Orchestrator exception catching |
