import pickle
import joblib
import os
import math

class RecommendationEngine:
    """
    Data-Driven Apex Engine converting sub-AI matrices into operational actions.
    """
    def __init__(self, model_path='ai_engine/saved_models/recommendation_engine.pkl'):
        if os.path.exists(model_path):
            try:
                self.model_data = joblib.load(model_path)
            except (FileNotFoundError, EOFError, pickle.UnpicklingError, Exception) as e:
                from ai_monitoring.services import LoggingService
                LoggingService.log_prediction(
                    module_name=self.__class__.__name__,
                    request_source='SYSTEM',
                    input_payload={},
                    output_payload=None,
                    confidence=0,
                    response_time=0,
                    status='ERROR',
                    error_message=f"Model loading failed: {str(e)}",
                    endpoint='STARTUP'
                )
                from ai_engine.exceptions import AIUnavailableException
                raise AIUnavailableException("AI model unavailable")
            self.thresholds = self.model_data['score_thresholds']
            self.action_coeffs = self.model_data['action_coefficients']
            self.esc_bounds = self.model_data['escalation_bounds']
        else:
            self.model_data = None

    def evaluate_city(self, ward_payloads):
        """Processes multiple wards for a city-wide summary."""
        city_summary = {}
        for payload in ward_payloads:
            result = self.generate_recommendations(payload)
            city_summary[result["ward"]] = result["priority_level"]
            
        # Sort by severity theoretically
        priority_map = {"Extreme": 5, "Critical": 4, "High": 3, "Moderate": 2, "Low": 1}
        sorted_city = dict(sorted(city_summary.items(), key=lambda x: priority_map.get(x[1], 0), reverse=True))
        return sorted_city

    def generate_recommendations(self, payload):
        """
        payload is defined by RECOMMENDATION_DATA_CONTRACT.
        """
        if not self.model_data:
            raise ValueError("Recommendation model not trained.")
            
        w = payload.get("ward", "Unknown")
        f_prob = payload.get("flood_probability", 0.0)
        w_risk = payload.get("ward_risk_score", 0.0)
        r_short = payload.get("resource_shortage_score", 0.0)
        b_risk = payload.get("building_risk_score", 0.0)
        f_inc = float(payload.get("forecast_incidents", 0.0))
        f_sev = payload.get("forecast_severity_critical_pct", 0.0)

        # 1. Feature Engineering (Mathematical Composites)
        # Weighting based on immediate threat vs systemic threat
        combined_risk_score = (f_prob * 0.3) + (w_risk * 0.3) + (b_risk * 0.2) + (min(100.0, f_inc) * 0.2)
        combined_risk_score = min(100.0, max(0.0, combined_risk_score))
        
        # Escalation score amplifies base risk based on inability to respond (shortage)
        escalation_score = combined_risk_score * (1.0 + (r_short / 100.0))
        escalation_score = min(100.0, max(0.0, escalation_score))
        
        # 2. Priority Engine (Using Learned Thresholds)
        if combined_risk_score >= self.thresholds["Extreme"]: p_level = "Extreme"
        elif combined_risk_score >= self.thresholds["Critical"]: p_level = "Critical"
        elif combined_risk_score >= self.thresholds["High"]: p_level = "High"
        elif combined_risk_score >= self.thresholds["Moderate"]: p_level = "Moderate"
        else: p_level = "Low"
        
        # 3. Escalation Engine
        if escalation_score >= self.esc_bounds["Control Room Escalation"]:
            esc_level = "Control Room Escalation"
        elif escalation_score >= self.esc_bounds["Emergency Action"]:
            esc_level = "Emergency Action"
        elif escalation_score >= self.esc_bounds["Department Action"]:
            esc_level = "Department Action"
        elif escalation_score >= self.esc_bounds["Monitor"]:
            esc_level = "Monitor"
        else:
            esc_level = "No Action"

        # 4. Action Recommendation Matrix
        # Calculate confidence scores for every possible action using learned coefficients
        generated_actions = []
        for action_name, coeffs in self.action_coeffs.items():
            confidence = (
                (coeffs.get("flood", 0) * f_prob) +
                (coeffs.get("ward_risk", 0) * w_risk) +
                (coeffs.get("shortage", 0) * r_short) +
                (coeffs.get("building", 0) * b_risk) +
                (coeffs.get("forecast", 0) * min(100.0, f_inc)) +
                (coeffs.get("severity_pct", 0) * f_sev)
            )
            
            # If confidence crosses a nominal threshold (e.g., 50.0), recommend it
            if confidence >= 40.0:
                # Generate explanation referencing explicit inputs
                reasons = []
                if coeffs.get("flood", 0) > 0 and f_prob > 50: reasons.append(f"Flood Probability [{f_prob}%]")
                if coeffs.get("shortage", 0) > 0 and r_short > 50: reasons.append(f"Resource Shortage [{r_short}%]")
                if coeffs.get("building", 0) > 0 and b_risk > 50: reasons.append(f"Building Risk [{b_risk}%]")
                if coeffs.get("severity_pct", 0) > 0 and f_sev > 20: reasons.append(f"Critical Severity Forecast [{f_sev}%]")
                if coeffs.get("forecast", 0) > 0 and f_inc > 30: reasons.append(f"Forecasted Incident Surge [{int(f_inc)} events]")
                if coeffs.get("ward_risk", 0) > 0 and w_risk > 60: reasons.append(f"Ward Vulnerability [{w_risk}%]")
                
                reason_str = "Driven by: " + ", ".join(reasons) if reasons else "Routine data-driven precaution."
                
                # Priority of action is inverse of confidence (higher confidence = Priority 1)
                a_priority = 1 if confidence > 80 else (2 if confidence > 60 else 3)
                
                generated_actions.append({
                    "action": action_name,
                    "priority": a_priority,
                    "confidence": float(round(min(100.0, confidence), 1)),
                    "reason": reason_str
                })
                
        # Fallback if no specific actions triggered
        if not generated_actions:
            generated_actions.append({
                "action": "Maintain Standard Vigilance",
                "priority": 4,
                "confidence": 99.0,
                "reason": "Risk signals below operational thresholds."
            })

        # Sort actions by confidence
        generated_actions.sort(key=lambda x: x["confidence"], reverse=True)

        return {
            "ward": w,
            "combined_risk_score": float(round(combined_risk_score, 1)),
            "priority_level": p_level,
            "escalation_level": esc_level,
            "recommendations": generated_actions
        }
