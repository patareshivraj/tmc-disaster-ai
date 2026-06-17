# Enterprise Copilot Architecture

## Overview
The TMC Disaster Management Copilot has been upgraded to a true enterprise-grade AI operations assistant. Instead of acting as a simple Q&A bot, it now performs dynamic, multi-step reasoning by orchestrating the underlying deterministic AI models sequentially or in parallel.

## Architectural Changes
1. **Multi-Tool Reasoning Engine:** The `CopilotEngine` now utilizes an iterative execution loop (up to 5 max iterations). This allows the LLM to request multiple tools simultaneously, wait for their responses, synthesize the data, and make follow-up tool calls if more context is needed.
2. **Deterministic Fallback Integration:** The fallback mechanism acts as a safety net. If the LLM layer fails, the `ChatbotEngine` catches the query, ensuring zero downtime.
3. **Enhanced Prompting Strategy:** The `SYSTEM_PROMPT` enforces entity resolution, explainability constraints, and mandates uncertainty disclosures (e.g., using "estimates" instead of "will").
4. **Tool Router Enhancements:** The `ToolRouter` now supports fetching the top 5 most critical buildings for an entire ward natively without bypassing the deterministic risk logic.

## Information Flow
1. User asks a complex question.
2. The `CopilotEngine` loops, sending the query to the OpenAI Provider.
3. The LLM requests multiple tools (e.g., `get_ward_status` and `get_incident_forecast`).
4. The `ToolRouter` triggers the deterministic engines.
5. The `CopilotEngine` aggregates JSON results back into the messages context.
6. The LLM synthesizes an evidence-based executive summary.
7. Logs are captured via `LLMInteractionLog`.
