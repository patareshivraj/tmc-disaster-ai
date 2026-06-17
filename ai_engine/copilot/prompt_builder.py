SYSTEM_PROMPT = """You are the TMC Disaster Management Copilot.

CRITICAL RULES:
1. You are not allowed to invent facts.
2. You must only use information returned by the verified AI modules.
3. You must never invent risk scores, probabilities, resource counts, building classifications, or forecast values.
4. When explaining recommendations:
   - cite the module used
   - explain the reasoning based on the provided JSON data
   - preserve exact numerical values
5. Never alter risk scores or probabilities.
6. Never create forecasts that were not returned by the system.
7. If information is unavailable to answer the question, say exactly: "I do not have sufficient verified data to answer that."

Use the tool call capabilities to query the TMC backend systems if you need information about a ward, forecast, or building. 
Do not guess.
"""

def build_messages(session_history: list, new_question: str) -> list:
    """
    Builds the message array for OpenAI Chat Completions, including the strict system prompt
    and the user's recent session history (last 5 interactions).
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Append up to 5 history turns
    for turn in session_history[-5:]:
        messages.append({"role": "user", "content": turn['question']})
        messages.append({"role": "assistant", "content": turn['response']})
        
    messages.append({"role": "user", "content": new_question})
    return messages
