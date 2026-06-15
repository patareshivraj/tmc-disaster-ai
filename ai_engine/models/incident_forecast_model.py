import joblib
import os
import pandas as pd
from datetime import datetime, timedelta
import math

class IncidentForecastEngine:
    """
    Data-Driven Time-Series Forecaster for Municipal Disasters.
    """
    def __init__(self, model_path='ai_engine/saved_models/incident_forecast.pkl'):
        if os.path.exists(model_path):
            self.model_data = joblib.load(model_path)
            self.base_daily_rate = self.model_data['base_daily_rate']
            self.seasonality = self.model_data['seasonality_multipliers']
            self.cat_dist = self.model_data['category_distributions']
            self.sev_dist = self.model_data['severity_distributions']
            self.ward_dist = self.model_data['ward_distributions']
        else:
            self.model_data = None

    def forecast_incidents(self, days, target_date=None, weather_modifier=1.0, resource_shortage=False):
        if not self.model_data:
            raise ValueError("Forecast model not trained.")
            
        if target_date is None:
            target_date = datetime.now()
            
        # 1. Temporal Window Analysis
        # Calculate exactly which months we are traversing to get a perfect blend of seasonality
        forecast_end = target_date + timedelta(days=days)
        months_covered = []
        current = target_date
        while current <= forecast_end:
            if current.month not in months_covered:
                months_covered.append(current.month)
            current += timedelta(days=5) # Step to ensure we capture all month overlaps safely
            
        if forecast_end.month not in months_covered:
            months_covered.append(forecast_end.month)
            
        # 2. Seasonality & Trend Calculation
        avg_seasonality = sum([self.seasonality.get(m, 1.0) for m in months_covered]) / len(months_covered)
        
        # Apply weather and resource modifiers mathematically
        trend_multiplier = avg_seasonality * weather_modifier
        if resource_shortage:
            trend_multiplier *= 1.15 # 15% bump due to resource stress exacerbating minor incidents into registered ones
            
        expected_incidents_raw = self.base_daily_rate * days * trend_multiplier
        expected_incidents = math.ceil(expected_incidents_raw)
        
        # 3. Aggregating Distributions
        # Average the categorical probabilities across the months covered
        combined_cats = {}
        combined_sevs = {}
        combined_wards = {}
        
        for m in months_covered:
            for k, v in self.cat_dist.get(m, {}).items(): combined_cats[k] = combined_cats.get(k, 0) + v
            for k, v in self.sev_dist.get(m, {}).items(): combined_sevs[k] = combined_sevs.get(k, 0) + v
            for k, v in self.ward_dist.get(m, {}).items(): combined_wards[k] = combined_wards.get(k, 0) + v
            
        # Normalize
        for k in combined_cats: combined_cats[k] /= len(months_covered)
        for k in combined_sevs: combined_sevs[k] /= len(months_covered)
        for k in combined_wards: combined_wards[k] /= len(months_covered)

        # Apply expected count to categories
        category_forecast = {k: math.ceil(v * expected_incidents) for k, v in combined_cats.items()}
        severity_distribution = {k: round(v * 100.0, 1) for k, v in combined_sevs.items()}
        
        # 4. Hotspot Prediction
        # Sort wards by expected probability to find the top 5
        sorted_wards = sorted(combined_wards.items(), key=lambda x: x[1], reverse=True)
        hotspots = [w for w, score in sorted_wards[:5]]
        
        # 5. Explainability
        explanations = [
            f"Base historical volume calculated at {round(self.base_daily_rate, 2)} daily incidents.",
            f"Learned seasonality multiplier for overlapping months is {round(avg_seasonality, 2)}x normal volume."
        ]
        if weather_modifier > 1.1:
            explanations.append(f"Severe weather trend applied ({round(weather_modifier, 2)}x).")
        elif weather_modifier < 0.9:
            explanations.append(f"Dry/Stable weather trend applied ({round(weather_modifier, 2)}x).")
            
        if resource_shortage:
            explanations.append("High resource shortage detected: Escalation risk applied.")

        return {
            "forecast_period": f"{days}_days",
            "expected_incidents": expected_incidents,
            "hotspots": hotspots,
            "category_forecast": category_forecast,
            "severity_distribution": severity_distribution,
            "explanations": explanations
        }
