import os
from typing import Dict, Any, List, Optional
from ai_engine.llm.base import LLMProvider
from openai import OpenAI, APIError, RateLimitError, APITimeoutError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class OpenAIProvider(LLMProvider):
    def __init__(self):
        # Using Groq via OpenAI client for validation due to quota issues
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        self.model = os.environ.get("OPENAI_MODEL", "llama-3.3-70b-versatile")
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.groq.com/openai/v1")

    @retry(
        retry=retry_if_exception_type((APIError, RateLimitError, APITimeoutError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def generate(self, messages: List[Dict[str, str]], tools: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Call OpenAI ChatCompletions API with retries and timeout.
        """
        # If the API key is totally missing or invalid, it might fail quickly. 
        # But this is a generic implementation.
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.0, # Zero temperature to minimize hallucinations
        }
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        response = self.client.chat.completions.create(**kwargs)
        
        choice = response.choices[0].message
        
        return {
            "content": choice.content,
            "tool_calls": choice.tool_calls,
            "token_usage": response.usage.total_tokens if response.usage else 0,
            "model_name": response.model
        }
