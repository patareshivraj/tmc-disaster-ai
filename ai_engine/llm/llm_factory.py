from ai_engine.llm.base import LLMProvider
from ai_engine.llm.openai_provider import OpenAIProvider

class LLMFactory:
    @staticmethod
    def get_provider() -> LLMProvider:
        # In a real system, you could check an environment variable like LLM_PROVIDER
        # and instantiate AnthropicProvider, GeminiProvider, etc.
        return OpenAIProvider()
