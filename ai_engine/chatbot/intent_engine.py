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
        
        extracted_ward = self.extract_ward(query)
        detected_intents = []
        
        for intent, patterns in self.intent_patterns.items():
            for p in patterns:
                if re.search(p, q_lower):
                    detected_intents.append(intent)
                    break
                    
        # Primary intent resolution
        if "Emergency" in detected_intents:
            primary_intent = "Emergency"
        elif "City-Wide" in detected_intents:
            primary_intent = "City-Wide"
        elif "Recommendation" in detected_intents:
            primary_intent = "Recommendation"
        elif "Forecast" in detected_intents:
            primary_intent = "Forecast"
        elif "Resource" in detected_intents:
            primary_intent = "Resource"
        elif "Building" in detected_intents:
            primary_intent = "Building"
        elif "Ward Risk" in detected_intents:
            primary_intent = "Ward Risk"
        elif "Flood" in detected_intents:
            primary_intent = "Flood"
        else:
            primary_intent = "General"
            
        return {
            "primary_intent": primary_intent,
            "all_intents": detected_intents,
            "target_ward": extracted_ward
        }
