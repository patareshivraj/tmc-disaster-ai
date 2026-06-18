from ai_engine.llm.base import LLMProvider

class LLMFactory:
    @staticmethod
    def get_provider() -> LLMProvider:
        import os
        provider = os.environ.get("LLM_PROVIDER", "gemini").lower()
        if provider == "openai":
            from ai_engine.llm.openai_provider import OpenAIProvider
            return OpenAIProvider()
        elif provider == "gemini":
            from ai_engine.llm.gemini_provider import GeminiProvider
            return GeminiProvider()
        else:
            raise ValueError(f"Provider {provider} not supported.")
