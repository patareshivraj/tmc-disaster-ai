import pytest
from unittest.mock import patch, MagicMock
from ai_engine.copilot.copilot_engine import CopilotEngine

@pytest.mark.django_db
def test_uncertainty_disclosure():
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
                "content": "Flood AI estimates an 81.3% probability of flooding in Diva.",
                "tool_calls": [],
                "token_usage": 30,
                "model_name": "gpt-4-test"
            }
        ]
        
        res = engine.process_query("test_session_uncert", "Will it flood in Diva?")
        
        assert "estimates" in res["answer"].lower() or "probability" in res["answer"].lower()
        assert "will flood" not in res["answer"].lower() # It should not state it as absolute fact
