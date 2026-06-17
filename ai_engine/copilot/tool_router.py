import json
from ai_engine.chatbot.chatbot_orchestrator import ChatbotOrchestrator

class ToolRouter:
    def __init__(self):
        self.orchestrator = ChatbotOrchestrator()
        
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_ward_status",
                    "description": "Get the comprehensive disaster risk status, recommendations, and flood probability for a specific ward.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ward": {
                                "type": "string",
                                "description": "The name of the ward, e.g. 'Diva', 'Kalwa'."
                            }
                        },
                        "required": ["ward"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_city_summary",
                    "description": "Get the disaster status summary for all wards in the city."
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_resource_allocation",
                    "description": "Get the resource gaps and allocation recommendations (pumps, boats, vehicles) for a specific ward.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ward": {
                                "type": "string",
                                "description": "The name of the ward, e.g. 'Diva'."
                            }
                        },
                        "required": ["ward"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_incident_forecast",
                    "description": "Forecast incident volumes over a number of days.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "days": {
                                "type": "integer",
                                "description": "Number of days to forecast for."
                            }
                        },
                        "required": ["days"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_building_risk",
                    "description": "Get structural risk for an individual building ID or general building risk."
                }
            }
        ]

    def get_tools(self):
        return self.tools

    def execute_tool(self, tool_call) -> str:
        """
        Execute a tool requested by the LLM and return its JSON response as a string.
        """
        name = tool_call.function.name
        
        # If no arguments provided, arguments string might be empty
        try:
            arguments = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
        except json.JSONDecodeError:
            arguments = {}

        try:
            if name == "get_ward_status":
                ward = arguments.get("ward", "Diva")
                # Emulate the Emergency/Ward Risk intent logic
                res = self.orchestrator.execute({"primary_intent": "Emergency", "target_ward": ward})
                return json.dumps(res)
                
            elif name == "get_city_summary":
                res = self.orchestrator.execute({"primary_intent": "City-Wide", "target_ward": None})
                return json.dumps(res)
                
            elif name == "get_resource_allocation":
                ward = arguments.get("ward", "Diva")
                res = self.orchestrator.execute({"primary_intent": "Resource", "target_ward": ward})
                return json.dumps(res)
                
            elif name == "get_incident_forecast":
                res = self.orchestrator.execute({"primary_intent": "Forecast", "target_ward": None})
                return json.dumps(res)
                
            elif name == "get_building_risk":
                res = self.orchestrator.execute({"primary_intent": "Building", "target_ward": None})
                return json.dumps(res)
                
            else:
                return json.dumps({"error": f"Tool {name} not found."})
                
        except Exception as e:
            return json.dumps({"error": str(e)})
