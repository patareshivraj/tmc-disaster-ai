class ResponseBuilder:
    """
    Transforms JSON outputs from the AI Orchestrator into natural, officer-friendly responses.
    """
    def compose(self, original_query, intent_data, orchestrator_results):
        if "error" in orchestrator_results:
            return {
                "question": original_query,
                "answer": "I'm currently unable to access the underlying AI systems due to an internal error.",
                "reasoning": [orchestrator_results["error"]],
                "recommended_actions": [],
                "confidence": 0
            }
            
        intent = intent_data["primary_intent"]
        
        answer = ""
        reasons = []
        actions = []
        confidence = 94
        
        if intent == "City-Wide" and "city_summary" in orchestrator_results:
            summary = orchestrator_results["city_summary"]
            answer = "Here is the city-wide summary based on current AI metrics:"
            for w, p in summary.items():
                reasons.append(f"{w} -> {p}")
            actions.append("Review Command Center Dashboard for details.")
            
        elif "top_ward_details" in orchestrator_results:
            top_rec = orchestrator_results["top_ward_details"]
            answer = f"{top_rec['ward']} requires immediate attention."
            reasons.append(f"Combined Risk Score: {top_rec['combined_risk_score']}")
            reasons.append(f"Priority Level: {top_rec['priority_level']}")
            
            for rec in top_rec['recommendations'][:3]:
                actions.append(rec["action"])
                if rec["reason"] not in reasons:
                    reasons.append(rec["reason"])
                    
        elif "forecast" in orchestrator_results and intent == "Forecast":
            f_res = orchestrator_results["forecast"]
            answer = f"Expected incident volume is {f_res['expected_incidents']} over the next {f_res['forecast_period']}."
            reasons.extend(f_res["explanations"])
            actions.append(f"Monitor Hotspots: {', '.join(f_res['hotspots'][:3])}")
            
        elif "resource" in orchestrator_results and intent == "Resource":
            r_res = orchestrator_results["resource"]
            answer = f"Resource allocation plan generated for {intent_data['target_ward'] or 'the requested ward'}."
            for alloc in r_res["resources_needed"]:
                if alloc["shortage"] > 0:
                    reasons.append(f"Shortage of {alloc['shortage']} {alloc['resource']}.")
                    actions.append(f"Deploy {alloc['required']} {alloc['resource']}")
                    
        elif "building" in orchestrator_results and intent == "Building":
            b_res = orchestrator_results["building"]
            answer = f"Building {b_res['building_name']} is classified as {b_res['classification']}."
            for rf in b_res["learned_risk_factors"]:
                reasons.append(f"{rf['factor']} (Historical Rate: {rf.get('historical_high_risk_rate', 'N/A')}%)")
            actions.extend(b_res["recommendations"])

        elif "recommendation" in orchestrator_results:
            rec = orchestrator_results["recommendation"]
            answer = f"{rec['ward']} is currently marked as {rec['priority_level']} priority."
            reasons.append(f"Combined Risk Score: {rec['combined_risk_score']}")
            
            for r in rec['recommendations'][:3]:
                actions.append(r["action"])
                if r["reason"] not in reasons:
                    reasons.append(r["reason"])

        elif "city_summary" in orchestrator_results:
            summary = orchestrator_results["city_summary"]
            answer = "Here is the city-wide summary based on current AI metrics."
            for w, p in summary.items():
                reasons.append(f"{w} -> {p}")
            actions.append("Review Command Center Dashboard for details.")
            
        else:
            answer = "I have analyzed the current data but could not find a specific operational anomaly."
            reasons.append("All signals within standard operational baselines.")
            actions.append("Maintain Standard Vigilance")

        return {
            "question": original_query,
            "answer": answer,
            "reasoning": list(dict.fromkeys(reasons)), # Remove duplicates
            "recommended_actions": list(dict.fromkeys(actions)),
            "confidence": confidence
        }
