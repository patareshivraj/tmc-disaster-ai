# LLM SECURITY & RELIABILITY GUIDE

## 1. Authentication & Key Management
*   **Key Storage:** The `OPENAI_API_KEY` is completely abstracted from the codebase. It is pulled strictly from the OS Environment variables (or `.env`).
*   **Model Enforcement:** The application defaults to `gpt-4o-mini` to balance latency and intelligence. This is configurable via `OPENAI_MODEL` in the environment.

## 2. API Resilience & Rate Limiting
The `OpenAIProvider` utilizes the `tenacity` Python library to gracefully handle network degradation.
*   **Retry Logic:** Automatically retries up to 3 times on `APIError`, `RateLimitError`, and `APITimeoutError`.
*   **Exponential Backoff:** Introduces a compounding delay (e.g., 2s, 4s, 8s) between retries to prevent spamming the OpenAI rate limit tier.
*   **Zero Temperature Constraint:** The `temperature` parameter is locked to `0.0`. This enforces deterministic, highly focused responses, minimizing creative divergence and "jailbreak" potential.

## 3. Data Leakage & Session Security
*   **Rolling Memory Window:** To prevent context bloating and unintentional data bleeding across extended sessions, the `CopilotEngine` enforces a strict 5-turn maximum memory window.
*   **Cache Expire:** Session memory stored in `django.core.cache` expires automatically after 3600 seconds (1 hour).

## 4. Monitoring & Forensics
Every interaction is logged to the `LLMInteractionLog` database table.
**Tracked Metrics for SOC/DevOps:**
*   `tools_called`: Audit trail of what internal APIs the LLM requested.
*   `token_usage`: Track LLM spending and detect anomalous prompt injection attempts resulting in huge token dumps.
*   `response_time`: Ensure the API SLA remains under 2000ms.
*   `error_message`: Full stack trace if the OpenAI API or Internal API crashes.
