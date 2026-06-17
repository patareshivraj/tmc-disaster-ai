import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dmd_project.settings")
django.setup()

from django.test import TestCase
from unittest.mock import patch, MagicMock
from ai_engine.copilot.copilot_engine import CopilotEngine
from ai_engine.copilot.prompt_builder import build_messages
from ai_engine.copilot.tool_router import ToolRouter
from ai_monitoring.models import LLMInteractionLog

class TestCopilotEngine(TestCase):
    def setUp(self):
        self.engine = CopilotEngine()

    @patch('ai_engine.llm.openai_provider.OpenAIProvider.generate')
    def test_tool_calling_and_memory(self, mock_generate):
        # Mocking the first call to request a tool
        tool_call_mock = MagicMock()
        tool_call_mock.function.name = 'get_ward_status'
        tool_call_mock.function.arguments = '{"ward": "Diva"}'
        tool_call_mock.id = 'call_123'

        # We configure side_effect for two consecutive calls
        mock_generate.side_effect = [
            {
                "content": "",
                "tool_calls": [tool_call_mock],
                "token_usage": 10,
                "model_name": "gpt-4o-mini"
            },
            {
                "content": "Diva is currently at high risk.",
                "tool_calls": None,
                "token_usage": 20,
                "model_name": "gpt-4o-mini"
            }
        ]

        response = self.engine.process_query("session_1", "Which ward needs attention?")
        
        self.assertEqual(response["answer"], "Diva is currently at high risk.")
        self.assertIn("get_ward_status", response["tools_used"])
        self.assertEqual(response["token_usage"], 30)

        # Verify log was created
        log = LLMInteractionLog.objects.filter(session_id="session_1").first()
        self.assertIsNotNone(log)
        self.assertEqual(log.tools_called, ["get_ward_status"])

    def test_prompt_builder_hallucination_rules(self):
        messages = build_messages([], "Test question")
        system_prompt = messages[0]["content"]
        
        self.assertIn("CRITICAL RULES:", system_prompt)
        self.assertIn("never invent risk scores", system_prompt)
        self.assertIn("never alter risk scores", system_prompt.lower())

    @patch('ai_engine.llm.openai_provider.OpenAIProvider.generate')
    def test_graceful_degradation_on_failure(self, mock_generate):
        mock_generate.side_effect = Exception("OpenAI API is down")
        
        response = self.engine.process_query("session_2", "Help")
        
        self.assertEqual(response["confidence"], 0)
        self.assertIn("I do not have sufficient verified data to answer that", response["answer"])
        self.assertIn("error", response)

    def test_tool_router_valid_call(self):
        router = ToolRouter()
        
        tool_call_mock = MagicMock()
        tool_call_mock.function.name = 'get_city_summary'
        tool_call_mock.function.arguments = '{}'
        
        res_json = router.execute_tool(tool_call_mock)
        self.assertIn("city_summary", res_json)
