import pytest
from unittest.mock import patch
from ai_engine.copilot.copilot_engine import CopilotEngine

@pytest.mark.django_db
def test_memory_resolution():
    engine = CopilotEngine()
    
    with patch('ai_engine.llm.openai_provider.OpenAIProvider.generate') as mock_generate:
        # First query: "Which ward needs attention?"
        mock_generate.side_effect = [
            {
                "content": "Diva requires immediate attention.",
                "tool_calls": [],
                "token_usage": 20,
                "model_name": "gpt-4-test"
            },
            # Second query: "How many pumps should we deploy there?"
            {
                "content": "Deploy 2 pumps to Diva.",
                "tool_calls": [],
                "token_usage": 30,
                "model_name": "gpt-4-test"
            }
        ]
        
        res1 = engine.process_query("test_session_memory", "Which ward needs attention?")
        assert "Diva" in res1["answer"]
        
        # Second interaction uses memory
        res2 = engine.process_query("test_session_memory", "How many pumps should we deploy there?")
        assert "Diva" in res2["answer"]
        
        # Check that memory was passed to the LLM
        # mock_generate.call_args[0][0] contains the messages array
        messages = mock_generate.call_args[0][0]
        # Should contain system prompt + 1 history turn + current question
        assert len(messages) == 4
        assert messages[1]["content"] == "Which ward needs attention?"
        assert messages[2]["content"] == "Diva requires immediate attention."
        assert messages[3]["content"] == "How many pumps should we deploy there?"
