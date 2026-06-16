import pickle
import joblib
import os

class WardRiskEngine:
    """
    Data-Derived Hybrid Scoring Engine for Ward Vulnerability.
    Weights are computed via Coefficient of Variation, not manually assigned.
    """
    def __init__(self, model_path=None):
        if model_path is None:
            import os
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(base_dir, 'saved_models', 'ward_risk_model.pkl')
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
            self.baselines = self.model_data['ward_baselines']
            self.scalers = self.model_data['scalers']
            self.weights = self.model_data['weights']
        else:
            self.model_data = None

    def _normalize(self, val, metric):
        min_v = self.scalers[metric]['min']
        max_v = self.scalers[metric]['max']
        if max_v == min_v:
            return 0.5
        return (val - min_v) / (max_v - min_v)

    def _compute_confidence(self, factor_values):
        """
        Dynamic confidence based on factor certainty.
        Factors near 0.0 or 1.0 (extremes) indicate high certainty.
        Factors near 0.5 (middle) indicate maximum uncertainty.
        Confidence = average distance from 0.5, scaled to percentage.
        """
        certainties = []
        for val in factor_values:
            # Distance from maximum uncertainty (0.5)
            certainty = abs(val - 0.5) * 2.0  # Range: 0.0 (uncertain) to 1.0 (certain)
            certainties.append(certainty)
        # Scale: minimum 50% (we always have some data), maximum 99%
        raw_confidence = sum(certainties) / len(certainties) if certainties else 0.5
        return round(50.0 + (raw_confidence * 49.0), 1)

    def predict_ward_risk(self, ward):
        if not self.model_data:
            raise ValueError("Ward Risk model not built. Run train_ward_risk.py first.")

        if ward not in self.baselines:
            raise ValueError(f"Ward {ward} not found in historical baselines.")

        data = self.baselines[ward]

        # Calculate individual normalized risk factors (0.0 to 1.0)
        flood_factor = self._normalize(data['flood_count'], 'flood_count')
        incident_factor = self._normalize(data['incident_count'], 'incident_count')
        building_factor = self._normalize(data['building_risk_score'], 'building_risk_score')
        prep_factor = self._normalize(data['preparedness_score'], 'preparedness_score')
        response_factor = self._normalize(data['avg_response_time'], 'avg_response_time')
        weather_factor = self._normalize(data['weather_severity_score'], 'weather_severity_score')
        resource_factor = self._normalize(data['resource_consumption_score'], 'resource_consumption_score')

        # Apply data-derived weights
        raw_score = (
            (weather_factor * self.weights['weather_severity']) +
            (flood_factor * self.weights['flood_risk']) +
            (incident_factor * self.weights['incident_frequency']) +
            (building_factor * self.weights['building_risk']) +
            (resource_factor * self.weights['resource_shortage']) +
            (response_factor * self.weights['response_efficiency']) +
            (prep_factor * self.weights['preparedness_penalty'])
        )

        risk_score = max(0.0, min(100.0, (raw_score + 0.15) * 100))

        # Determine Level
        if risk_score > 75:
            risk_level = "Critical"
        elif risk_score > 50:
            risk_level = "High"
        elif risk_score > 25:
            risk_level = "Moderate"
        else:
            risk_level = "Low"

        # Dynamic confidence from factor certainty
        all_factors = [flood_factor, incident_factor, building_factor,
                       prep_factor, response_factor, weather_factor, resource_factor]
        confidence = self._compute_confidence(all_factors)

        # Explainability & Recommendations
        factors = []
        recommendations = []

        if weather_factor > 0.5:
            factors.append("High Weather Severity")
            recommendations.append("Increase Weather Monitoring")
        if flood_factor > 0.5:
            factors.append("Frequent Flooding")
            recommendations.append("Deploy Additional Pumps")
        if building_factor > 0.5:
            factors.append("High Building Risk")
            recommendations.append("Immediate Structural Audit")
        if resource_factor > 0.5:
            factors.append("High Resource Consumption (Shortage Risk)")
            recommendations.append("Reallocate Equipment & Vehicles")
        if response_factor > 0.5:
            factors.append("Slow Historical Response Time")
            recommendations.append("Pre-position Emergency Teams")
        if incident_factor > 0.5:
            factors.append("High Historical Incident Density")
            recommendations.append("Increase Emergency Staffing")
        if prep_factor < 0.4:
            factors.append("Low Preparedness Score")
            recommendations.append("Conduct Mock Drills")

        if not factors:
            factors.append("General Vulnerability Threshold Reached")
            recommendations.append("Maintain Standard Vigilance")

        return {
            "ward": ward,
            "risk_score": float(round(risk_score, 2)),
            "risk_level": risk_level,
            "confidence": confidence,
            "risk_factors": factors,
            "recommendations": recommendations
        }
