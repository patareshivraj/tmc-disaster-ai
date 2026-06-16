import pickle
import joblib
from ai_engine.repositories.factory import DataSourceFactory
import os
import pandas as pd
from datetime import datetime

class BuildingAdvisorEngine:
    """
    Data-Driven AI Engine for Building Safety and Structural Risk.
    """
    def __init__(self, model_path=None):
        if model_path is None:
            import os
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(base_dir, 'saved_models', 'buildings.csv')
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
            self.ward_exposure_baselines = self.model_data['ward_exposure_baselines']
            self.age_risk_coefficients = self.model_data['age_risk_coefficients']
            self.condition_risk_coefficients = self.model_data['condition_risk_coefficients']
            self.inspection_risk_coefficients = self.model_data['inspection_risk_coefficients']
            self.base_risk_rate = self.model_data['base_risk_rate']
        else:
            self.model_data = None
            
        if os.path.exists(data_path):
            self.buildings_df = DataSourceFactory.get_dataframe("buildings")
        else:
            self.buildings_df = None

    def _get_classification(self, score):
        if score <= 25: return "Safe"
        if score <= 50: return "Monitor"
        if score <= 70: return "Repair Recommended"
        if score <= 85: return "Structural Audit Required"
        return "Evacuation / Demolition Candidate"

    def evaluate_building_features(self, age, condition, last_inspection_years, flood_exposure_norm, fire_exposure_norm):
        """Core math logic for building risk evaluation using data-driven coefficients."""
        
        # 1. Fetch Empirical Coefficients
        if age <= 20: age_group = '0-20'
        elif age <= 40: age_group = '21-40'
        elif age <= 60: age_group = '41-60'
        else: age_group = '60+'
        age_prob = self.age_risk_coefficients.get(age_group, self.base_risk_rate)
        
        cond_prob = self.condition_risk_coefficients.get(condition, self.base_risk_rate)
        
        if last_inspection_years <= 1: insp_group = '0-1'
        elif last_inspection_years <= 3: insp_group = '2-3'
        elif last_inspection_years <= 5: insp_group = '4-5'
        else: insp_group = '5+'
        insp_prob = self.inspection_risk_coefficients.get(insp_group, self.base_risk_rate)
        
        # 2. Risk Score (Statistical Independent Probability of Union)
        # P(A U B U C) = 1 - P(not A)*P(not B)*P(not C)
        combined_prob = 1.0 - ((1.0 - age_prob) * (1.0 - cond_prob) * (1.0 - insp_prob))
        
        # Multiply by 100 and add geographical flood exposure risk
        risk_score_raw = (combined_prob * 100.0) + (flood_exposure_norm * 30.0)
        risk_score = min(100.0, max(0.0, risk_score_raw))
        
        # 3. Collapse Probability
        # Derived mathematically from the condition and age historical failure rates
        collapse_prob = (age_prob * cond_prob * 100.0) + (risk_score * 0.5)
        collapse_prob = min(100.0, max(0.0, collapse_prob))
        
        # 4. Classification
        classification = self._get_classification(risk_score)
        
        # 5. Explainability & Recommendations
        risk_factors = []
        recommendations = []
        
        # Explainability strictly uses learned statistics
        if age_prob > self.base_risk_rate:
            risk_factors.append({"factor": f"Age {age_group} Years", "historical_high_risk_rate": round(age_prob * 100, 1)})
            
        if cond_prob > self.base_risk_rate:
            risk_factors.append({"factor": f"Condition: {condition}", "historical_high_risk_rate": round(cond_prob * 100, 1)})
            
        if insp_prob > self.base_risk_rate:
            risk_factors.append({"factor": f"Inspection Delay: {last_inspection_years} years", "historical_high_risk_rate": round(insp_prob * 100, 1)})
            
        if flood_exposure_norm > 0.5:
            risk_factors.append({"factor": "High Flood Exposure Ward", "historical_high_risk_rate": "N/A"})
            
        if not risk_factors:
            risk_factors.append({"factor": "No critical vulnerabilities detected based on historical rates.", "historical_high_risk_rate": 0.0})

        # Recommendation mappings
        if classification == "Evacuation / Demolition Candidate":
            recommendations.append("Immediate Evacuation")
            recommendations.append("Demolition Assessment")
        elif classification == "Structural Audit Required":
            recommendations.append("Structural Audit")
            recommendations.append("Prepare Evacuation Plan")
        elif classification == "Repair Recommended":
            recommendations.append("Repair")
        elif classification == "Monitor":
            recommendations.append("Routine Monitoring")
        else:
            recommendations.append("Safe")

        # Dynamic confidence: certainty of each risk dimension
        # Coefficients near 0.0 or 1.0 = high certainty, near 0.5 = uncertain
        age_certainty = abs(age_prob - 0.5) * 2.0
        cond_certainty = abs(cond_prob - 0.5) * 2.0
        insp_certainty = abs(insp_prob - 0.5) * 2.0
        raw_confidence = (age_certainty + cond_certainty + insp_certainty) / 3.0
        confidence = round(50.0 + (raw_confidence * 49.0), 1)

        return {
            "risk_score": float(round(risk_score, 2)),
            "collapse_probability": float(round(collapse_prob, 2)),
            "classification": classification,
            "learned_risk_factors": risk_factors,
            "recommendations": recommendations,
            "confidence": confidence
        }

    def predict_building_risk(self, building_id):
        if not self.model_data or self.buildings_df is None:
            raise ValueError("Building model not trained or data missing.")
            
        bld_rows = self.buildings_df[self.buildings_df['building_id'] == building_id]
        if bld_rows.empty:
            raise ValueError(f"Building ID {building_id} not found.")
            
        bld = bld_rows.iloc[0]
        
        # Feature Extraction
        current_year = datetime.now().year
        age = current_year - bld['year_built']
        
        try:
            insp_year = datetime.strptime(bld['inspection_date'], "%Y-%m-%d").year
        except:
            insp_year = current_year - 5 # Default penalty if invalid date
        last_inspection_years = current_year - insp_year
        
        ward = bld['ward']
        if ward in self.ward_exposure_baselines:
            flood_exp = self.ward_exposure_baselines[ward]['flood_exposure_normalized']
            fire_exp = 0.5
        else:
            flood_exp = 0.5
            fire_exp = 0.5
            
        condition = bld['condition']
        
        evaluation = self.evaluate_building_features(age, condition, last_inspection_years, flood_exp, fire_exp)
        
        return {
            "building_id": building_id,
            "building_name": bld['building_name'],
            "ward": ward,
            "risk_score": evaluation["risk_score"],
            "collapse_probability": evaluation["collapse_probability"],
            "classification": evaluation["classification"],
            "learned_risk_factors": evaluation["learned_risk_factors"],
            "recommendations": evaluation["recommendations"],
            "confidence": evaluation["confidence"]
        }
