from ai_engine.llm.base import LLMProvider

class LLMFactory:
    @staticmethod
    def get_provider() -> LLMProvider:
        import os
        provider = os.environ.get("LLM_PROVIDER", "openai").lower()
        if provider == "openai":
            from ai_engine.llm.openai_provider import OpenAIProvider
            return OpenAIProvider()
        else:
            raise ValueError(f"Provider {provider} not supported.")
