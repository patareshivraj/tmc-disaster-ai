import pickle
import joblib
import pandas as pd
import os

class FloodPredictionEngine:
    """
    Consumes raw inference data, formats it into ML features, and runs Random Forest prediction.
    """
    def __init__(self, model_path=None):
        if model_path is None:
            import os
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(base_dir, 'saved_models', 'flood_prediction.pkl')
        if os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
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
        else:
            self.model = None

    def predict_flood_risk(self, ward, rainfall, humidity, water_level, temperature, previous_flood_count, is_monsoon, avg_3_day=None, avg_7_day=None):
        if not self.model:
            raise ValueError("Model not trained yet. Run train_flood_model.py first.")
            
        # Fallbacks for rolling averages if not supplied by the real-time caller
        if avg_3_day is None: avg_3_day = rainfall
        if avg_7_day is None: avg_7_day = rainfall
            
        input_data = pd.DataFrame([{
            'ward': ward,
            'rainfall_mm': rainfall,
            'humidity': humidity,
            'water_level_m': water_level,
            'temperature': temperature,
            '3_day_avg_rainfall': avg_3_day,
            '7_day_avg_rainfall': avg_7_day,
            'previous_flood_count': previous_flood_count,
            'is_monsoon': is_monsoon
        }])
        
        # Predict probability of class 1 (Flood)
        prob = self.model.predict_proba(input_data)[0][1] * 100
        
        if prob > 50:
            risk = "Critical"
        elif prob > 25:
            risk = "High"
        elif prob > 10:
            risk = "Moderate"
        else:
            risk = "Low"
            
        return {
            "ward": ward,
            "flood_probability": float(round(prob, 2)),
            "risk_level": risk,
            "confidence": float(round(max(self.model.predict_proba(input_data)[0]) * 100, 2))
        }
