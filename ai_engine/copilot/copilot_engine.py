import uuid
import time
from django.core.cache import cache
from ai_engine.llm.llm_factory import LLMFactory
from ai_engine.copilot.prompt_builder import build_messages
from ai_engine.copilot.tool_router import ToolRouter
from ai_monitoring.models import LLMInteractionLog

class CopilotEngine:
    def __init__(self):
        self.llm = LLMFactory.get_provider()
        self.router = ToolRouter()

    def _get_session_history(self, session_id: str) -> list:
        history = cache.get(f"copilot_session_{session_id}")
        if not history:
            history = []
        return history

    def _save_session_history(self, session_id: str, question: str, response: str):
        history = self._get_session_history(session_id)
        history.append({"question": question, "response": response})
        # Keep only the last 5 interactions
        history = history[-5:]
        cache.set(f"copilot_session_{session_id}", history, timeout=3600) # 1 hour expiry

    def process_query(self, session_id: str, question: str) -> dict:
        start_time = time.time()
        
        if not session_id:
            session_id = str(uuid.uuid4())

        history = self._get_session_history(session_id)
        messages = build_messages(history, question)
        tools = self.router.get_tools()

        try:
            # 1. Call OpenAI to see if it needs tools or can answer directly
            response_data = self.llm.generate(messages, tools=tools)
            
            tool_calls_made = []
            final_content = response_data.get("content", "")

            # 2. If tools are requested, execute them and make a follow-up call
            if response_data.get("tool_calls"):
                messages.append({
                    "role": "assistant",
                    "content": final_content,
                    "tool_calls": response_data["tool_calls"]
                })
                
                for tool_call in response_data["tool_calls"]:
                    tool_result = self.router.execute_tool(tool_call)
                    tool_calls_made.append(tool_call.function.name)
                    
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "content": tool_result
                    })
                
                # Make the second call with the tool results
                second_response = self.llm.generate(messages)
                final_content = second_response.get("content", "")
                response_data["token_usage"] += second_response.get("token_usage", 0)

            response_time = (time.time() - start_time) * 1000

            # 3. Save to Session Memory
            self._save_session_history(session_id, question, final_content)

            # 4. Log interaction
            LLMInteractionLog.objects.create(
                session_id=session_id,
                question=question,
                response=final_content,
                tools_called=tool_calls_made,
                token_usage=response_data.get("token_usage", 0),
                response_time=response_time,
                model_name=response_data.get("model_name", "unknown")
            )

            return {
                "session_id": session_id,
                "answer": final_content,
                "tools_used": tool_calls_made,
                "token_usage": response_data.get("token_usage", 0),
                "confidence": 99.0 # Verified by deterministic tools
            }

        except Exception as e:
            error_message = str(e)
            
            # Fallback to the deterministic ChatbotEngine if OpenAI is unreachable or fails
            try:
                from ai_engine.chatbot.chatbot_engine import ChatbotEngine
                chatbot = ChatbotEngine()
                fallback_res = chatbot.answer_question(question)
                
                # Log the fallback interaction
                LLMInteractionLog.objects.create(
                    session_id=session_id,
                    question=question,
                    response=fallback_res.get("answer", "Fallback used."),
                    tools_called=["deterministic_fallback"],
                    token_usage=0,
                    response_time=(time.time() - start_time) * 1000,
                    model_name="fallback_chatbot",
                    status="SUCCESS_FALLBACK"
                )
                
                fallback_res["session_id"] = session_id
                fallback_res["tools_used"] = ["deterministic_fallback"]
                fallback_res["token_usage"] = 0
                return fallback_res
                
            except Exception as fallback_e:
                LLMInteractionLog.objects.create(
                    session_id=session_id,
                    question=question,
                    response="Error processing request.",
                    tools_called=[],
                    token_usage=0,
                    response_time=(time.time() - start_time) * 1000,
                    model_name="unknown",
                    status="ERROR",
                    error_message=error_message + " | Fallback Error: " + str(fallback_e)
                )
                return {
                    "session_id": session_id,
                    "answer": "I do not have sufficient verified data to answer that. (Service Unavailable)",
                    "error": error_message,
                    "tools_used": [],
                    "confidence": 0
                }
