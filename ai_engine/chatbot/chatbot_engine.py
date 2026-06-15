from ai_engine.chatbot.intent_engine import IntentEngine
from ai_engine.chatbot.chatbot_orchestrator import ChatbotOrchestrator
from ai_engine.chatbot.response_builder import ResponseBuilder

class ChatbotEngine:
    """
    The Single Conversational Interface for the TMC Disaster Management AI Platform.
    """
    def __init__(self):
        self.intent_engine = IntentEngine()
        self.orchestrator = ChatbotOrchestrator()
        self.response_builder = ResponseBuilder()

    def detect_intent(self, query):
        return self.intent_engine.detect_intent(query)

    def route_query(self, parsed_intent):
        return self.orchestrator.execute(parsed_intent)

    def compose_response(self, query, parsed_intent, orchestrator_results):
        return self.response_builder.compose(query, parsed_intent, orchestrator_results)

    def answer_question(self, query):
        # 1. Parse natural language into structured intent
        parsed_intent = self.detect_intent(query)
        
        # 2. Silently query the required AIs
        orchestrator_results = self.route_query(parsed_intent)
        
        # 3. Format into officer-friendly text
        final_response = self.compose_response(query, parsed_intent, orchestrator_results)
        
        return final_response
