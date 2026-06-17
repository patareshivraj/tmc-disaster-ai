import pytest
from unittest.mock import patch, MagicMock
from ai_engine.copilot.copilot_engine import CopilotEngine

@pytest.mark.django_db
def test_operational_briefing():
    engine = CopilotEngine()
    
    with patch('ai_engine.llm.openai_provider.OpenAIProvider.generate') as mock_generate:
        mock_generate.side_effect = [
            {
                "content": "",
                "tool_calls": [
                    MagicMock(id="call_1", function=MagicMock(name="get_city_summary", arguments='{}')),
                    MagicMock(id="call_2", function=MagicMock(name="get_incident_forecast", arguments='{"days": 1}'))
                ],
                "token_usage": 20,
                "model_name": "gpt-4-test"
            },
            {
                "content": "Current Situation: Diva is critical. Forecast Outlook: 10 incidents expected.",
                "tool_calls": [],
                "token_usage": 60,
                "model_name": "gpt-4-test"
            }
        ]
        
        res = engine.process_query("test_session_brief", "Give me today's disaster briefing.")
        
        assert "Current Situation" in res["answer"]
        assert "Forecast Outlook" in res["answer"]
