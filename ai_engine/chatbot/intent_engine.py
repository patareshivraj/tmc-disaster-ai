import re

class IntentEngine:
    """
    Parses natural language queries to detect intent and extract entities.
    """
    def __init__(self):
        self.wards = ["Diva", "Kalwa", "Mumbra", "Wagle Estate", "Naupada-Kopri", "Majiwada-Manpada", "Vartak Nagar", "Uthalsar", "Lokmanya-Savarkar Nagar"]
        
        # Regex mappings for semantic routing
        self.intent_patterns = {
            "Emergency": [r"immediate attention", r"most vulnerable", r"emergency", r"what should we do immediately"],
            "City-Wide": [r"city summary", r"city-wide", r"overall", r"all wards"],
            "Recommendation": [r"what should.*do", r"recommend", r"actions"],
            "Forecast": [r"forecast", r"expected", r"next \d+ days", r"how many incidents"],
            "Resource": [r"pumps", r"boats", r"resources", r"shortage", r"deploy"],
            "Building": [r"building", r"evacuation", r"structural", r"dangerous"],
            "Ward Risk": [r"which ward", r"highest risk", r"ward risk"],
            "Flood": [r"flood", r"water logging", r"rain"]
        }

    def extract_ward(self, query):
        for w in self.wards:
            if w.lower() in query.lower():
                return w
        return None

    def detect_intent(self, query):
        q_lower = query.lower()
        
        # Out-of-Domain / Hallucination check
        disaster_vocab = ["ward", "flood", "rain", "water", "pump", "boat", "resource", "building", "forecast", "risk", "attention", "emergency", "city", "action", "officer", "evacuation", "deploy", "vulnerable", "focus", "need", "immediately"]
        if not any(word in q_lower for word in disaster_vocab):
            return {
                "primary_intent": "Unknown",
                "all_intents": ["Unknown"],
                "target_ward": None
            }
        
        extracted_ward = self.extract_ward(query)
        detected_intents = []
        
        # Enhanced semantic equivalents
        if any(w in q_lower for w in ["immediate attention", "most vulnerable", "urgent action", "what should we do immediately", "emergency"]):
            detected_intents.append("Emergency")
        if any(w in q_lower for w in ["city summary", "city-wide", "overall", "all wards"]):
            detected_intents.append("City-Wide")
        if any(w in q_lower for w in ["what should officers do", "where should officers focus", "recommend", "actions", "focus today"]):
            detected_intents.append("Recommendation")
        if any(w in q_lower for w in ["forecast", "expected", "next days", "how many incidents"]):
            detected_intents.append("Forecast")
        if any(w in q_lower for w in ["pump", "boat", "resource", "shortage", "deploy", "send more"]):
            detected_intents.append("Resource")
        if any(w in q_lower for w in ["building", "evacuation", "structural", "dangerous"]):
            detected_intents.append("Building")
        if any(w in q_lower for w in ["which ward", "highest risk", "ward risk", "area is most vulnerable"]):
            detected_intents.append("Ward Risk")
        if any(w in q_lower for w in ["flood", "water logging", "rain"]):
            detected_intents.append("Flood")
            
        # Primary intent resolution
        if "Emergency" in detected_intents:
            primary_intent = "Emergency"
        elif "City-Wide" in detected_intents:
            primary_intent = "City-Wide"
        elif "Recommendation" in detected_intents:
            primary_intent = "Recommendation"
        elif "Ward Risk" in detected_intents:
            primary_intent = "Ward Risk"
        elif "Resource" in detected_intents:
            primary_intent = "Resource"
        elif "Forecast" in detected_intents:
            primary_intent = "Forecast"
        elif "Building" in detected_intents:
            primary_intent = "Building"
        elif "Flood" in detected_intents:
            primary_intent = "Flood"
        else:
            primary_intent = "General"
            
        return {
            "primary_intent": primary_intent,
            "all_intents": detected_intents,
            "target_ward": extracted_ward
        }
