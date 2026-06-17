import pytest
from unittest.mock import patch, MagicMock
from ai_engine.copilot.copilot_engine import CopilotEngine

@pytest.mark.django_db
def test_explainability():
    engine = CopilotEngine()
    
    with patch('ai_engine.llm.openai_provider.OpenAIProvider.generate') as mock_generate:
        mock_generate.side_effect = [
            {
                "content": "",
                "tool_calls": [
                    MagicMock(id="call_1", function=MagicMock(name="get_ward_status", arguments='{"ward": "Diva"}'))
                ],
                "token_usage": 10,
                "model_name": "gpt-4-test"
            },
            {
                "content": "Diva is critical because the Ward Risk AI evaluated a risk score of 88.5 and Flood AI estimates 81.3% probability.",
                "tool_calls": [],
                "token_usage": 50,
                "model_name": "gpt-4-test"
            }
        ]
        
        res = engine.process_query("test_session_explain", "Explain why Diva is critical.")
        
        assert "Ward Risk AI" in res["answer"]
        assert "Flood AI" in res["answer"]
        assert "88.5" in res["answer"]
        assert "81.3%" in res["answer"]
