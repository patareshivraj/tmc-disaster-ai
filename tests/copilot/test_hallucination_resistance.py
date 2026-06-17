import pytest
from unittest.mock import patch
from ai_engine.copilot.copilot_engine import CopilotEngine

@pytest.mark.django_db
def test_hallucination_resistance():
    engine = CopilotEngine()
    
    with patch('ai_engine.llm.openai_provider.OpenAIProvider.generate') as mock_generate:
        mock_generate.side_effect = [
            {
                "content": "I do not have sufficient verified data to answer that.",
                "tool_calls": [],
                "token_usage": 15,
                "model_name": "gpt-4-test"
            }
        ]
        
        res = engine.process_query("test_session_hallucinate", "What is the alien invasion risk score for Mumbai?")
        
        assert "sufficient verified data" in res["answer"]
