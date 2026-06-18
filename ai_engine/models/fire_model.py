import math

class FirePredictionEngine:
    def __init__(self):
        # Base risk heuristics
        self.max_temp_baseline = 45.0  # Max realistic temperature for scaling
        self.min_humidity_baseline = 10.0 # Extremely dry humidity
        
    def predict_fire_risk(self, ward, temperature, humidity, historical_fire_count):
        """
        Predicts the probability of a fire breaking out based on weather conditions
        and historical ward-specific fire density.
        """
        risk_factors = []
        
        # 1. Temperature Risk (Higher is worse)
        # Normalizes temperature. e.g. 40 degrees = 40/45 = 0.88 risk
        temp_risk = min(1.0, temperature / self.max_temp_baseline)
        if temperature > 35.0:
            risk_factors.append(f"High Temperature ({temperature}°C) increases dry-brush and electrical fire risk.")
            
        # 2. Humidity Risk (Lower is worse)
        # Normalizes humidity. e.g. 20% humidity means 1.0 - (20/100) = 0.8 risk
        # Extremely low humidity spikes risk dramatically
        humidity_risk = 1.0 - (humidity / 100.0)
        if humidity < 30.0:
            risk_factors.append(f"Critically low humidity ({humidity}%) accelerates fire spread potential.")
            
        # 3. Ward Historical Baseline Risk
        # If a ward has a history of fires, its baseline goes up. Max cap at 50 historical fires.
        ward_history_risk = min(1.0, historical_fire_count / 50.0)
        if historical_fire_count > 10:
            risk_factors.append(f"Ward has a high historical frequency of fires ({historical_fire_count} past incidents).")

        # 4. Composite Probability Calculation
        # Weights: Temperature is primary trigger (50%), Humidity accelerates (30%), Ward History sets baseline (20%)
        composite_score = (temp_risk * 0.50) + (humidity_risk * 0.30) + (ward_history_risk * 0.20)
        
        # Convert to percentage
        fire_probability = round(composite_score * 100.0, 2)
        
        # Clamp between 0.0 and 99.99
        fire_probability = max(0.0, min(99.99, fire_probability))
        
        # Determine Severity Level
        if fire_probability > 75.0:
            severity = "Critical"
        elif fire_probability > 50.0:
            severity = "High"
        elif fire_probability > 25.0:
            severity = "Moderate"
        else:
            severity = "Low"

        if not risk_factors:
            risk_factors.append("Optimal weather conditions. Low fire risk.")

        return {
            "ward": ward,
            "fire_probability": fire_probability,
            "severity_level": severity,
            "temperature_input": temperature,
            "humidity_input": humidity,
            "risk_factors": risk_factors
        }
