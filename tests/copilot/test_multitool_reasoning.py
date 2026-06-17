import pytest
from unittest.mock import patch, MagicMock
from ai_engine.copilot.copilot_engine import CopilotEngine

@pytest.mark.django_db
def test_multitool_reasoning():
    engine = CopilotEngine()
    
    # We will mock the LLM factory to return specific tool calls
    with patch('ai_engine.llm.openai_provider.OpenAIProvider.generate') as mock_generate:
        # First iteration: Request 2 tools
        mock_generate.side_effect = [
            {
                "content": "",
                "tool_calls": [
                    MagicMock(id="call_1", function=MagicMock(name="get_ward_status", arguments='{"ward": "Diva"}')),
                    MagicMock(id="call_2", function=MagicMock(name="get_incident_forecast", arguments='{"days": 7}'))
                ],
                "token_usage": 50,
                "model_name": "gpt-4-test"
            },
            # Second iteration: Return final synthesis
            {
                "content": "Diva has a risk score of 88.5 and we expect 42 incidents in the next 7 days.",
                "tool_calls": [],
                "token_usage": 100,
                "model_name": "gpt-4-test"
            }
        ]
        
        res = engine.process_query("test_session_multi", "Why is Diva critical and what is the forecast?")
        
        assert "Diva" in res["answer"]
        assert "get_ward_status" in res["tools_used"]
        assert "get_incident_forecast" in res["tools_used"]
        assert len(res["tools_used"]) == 2
        assert res["token_usage"] == 150
