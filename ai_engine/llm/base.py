from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, messages: List[Dict[str, str]], tools: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Generate a response from the LLM.
        Returns a dict containing:
        - content: str (the response text)
        - tool_calls: list (any tools requested by the model)
        - token_usage: int (total tokens used)
        - model_name: str
        """
        pass
