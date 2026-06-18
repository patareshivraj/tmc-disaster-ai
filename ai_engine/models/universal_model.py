import datetime
from django.db import connection

class UniversalPredictionEngine:
    def __init__(self):
        # We classify certain disasters as weather-driven.
        # Everything else falls to baseline historical frequency.
        self.weather_driven_categories = ['Flood', 'Fire', 'Electric Hazard', 'Tree Fall', 'Heat Wave']
        
    def _fetch_ward_disaster_history(self, ward_name):
        """
        Dynamically fetches the exact historical count of every disaster type 
        for the given ward directly from the live database.
        """
        history = {}
        try:
            with connection.cursor() as cursor:
                # Get all unique disaster categories dynamically
                cursor.execute("SELECT name FROM dmd_disaster_category")
                categories = [row[0] for row in cursor.fetchall()]
                
                # Fetch incident counts for this specific ward mapped to categories
                cursor.execute('''
                    SELECT c.name, COUNT(i.id) 
                    FROM dmd_disaster_category c
                    LEFT JOIN dmd_incident i ON c.id = i.disaster_category_id 
                    LEFT JOIN dmd_ward w ON i.ward_id = w.id AND w.name = %s
                    GROUP BY c.name
                ''', [ward_name])
                
                for row in cursor.fetchall():
                    history[row[0]] = row[1]
                    
                # Ensure all categories exist in dict even if 0 count
                for cat in categories:
                    if cat not in history:
                        history[cat] = 0
                        
        except Exception as e:
            print(f"Error fetching historical disaster data: {e}")
        return history

    def predict_all_threats(self, ward, temperature, humidity, rainfall, water_level, is_monsoon):
        """
        Calculates probabilities for ALL disasters dynamically.
        Separates them into Active Weather Threats and Baseline Historical Risks.
        """
        history = self._fetch_ward_disaster_history(ward)
        if not history:
            return {"error": "Could not connect to database or ward not found."}
            
        active_weather_threats = []
        historical_baseline_risks = []
        
        # Max incidents heuristic for baseline scaling (e.g. 500 incidents = 40% baseline risk cap)
        MAX_INCIDENT_CAP = 500.0 

        for disaster, count in history.items():
            probability = 0.0
            severity = "Low"
            risk_factors = []
            
            # Base probability derived purely from historical frequency in this ward
            # We cap historical risk at 40% so that live weather data drives the spikes
            baseline_prob = min(40.0, (count / MAX_INCIDENT_CAP) * 40.0)
            probability = baseline_prob
            
            is_weather_driven = False

            # --- WEATHER DRIVEN AI HEURISTICS ---
            if disaster == 'Flood' or disaster == 'Water Logging':
                is_weather_driven = True
                if rainfall > 50.0:
                    probability += (rainfall / 100.0) * 50  # Add up to 50% extra probability based on heavy rain
                    risk_factors.append(f"Heavy rainfall ({rainfall}mm) detected.")
                if water_level > 2.0:
                    probability += 25.0
                    risk_factors.append(f"Water level elevated ({water_level}m).")
                if is_monsoon == 1:
                    probability += 10.0
                    
            elif disaster == 'Fire' or disaster == 'Electric Hazard':
                is_weather_driven = True
                if temperature > 38.0:
                    probability += ((temperature - 38.0) / 10.0) * 40  # Scales up rapidly above 38C
                    risk_factors.append(f"High temperature ({temperature}°C) increases dry-brush/electrical risk.")
                if humidity < 25.0:
                    probability += 20.0
                    risk_factors.append(f"Low humidity ({humidity}%) accelerates spread.")
                    
            elif disaster == 'Tree Fall':
                is_weather_driven = True
                if is_monsoon == 1 and rainfall > 30.0:
                    probability += 35.0
                    risk_factors.append("Monsoon rains weaken soil, increasing tree fall risk.")
                    
            elif disaster == 'Heat Wave':
                is_weather_driven = True
                if temperature > 40.0:
                    probability += 80.0
                    risk_factors.append(f"Extreme temperature ({temperature}°C) triggers Heat Wave protocol.")
                    
            # Cap at 99.9%
            probability = min(99.9, round(probability, 2))
            
            # Determine Severity
            if probability >= 75.0: severity = "Critical"
            elif probability >= 50.0: severity = "High"
            elif probability >= 25.0: severity = "Moderate"
            else: severity = "Low"
            
            # Formatting reasons
            if not risk_factors:
                if count > 0:
                    risk_factors.append(f"Ward has historical baseline risk ({count} past incidents).")
                else:
                    risk_factors.append("No immediate active weather triggers or historical risk.")
            
            threat_payload = {
                "disaster": disaster,
                "probability": probability,
                "severity_level": severity,
                "historical_count_in_ward": count,
                "risk_factors": risk_factors
            }

            if is_weather_driven:
                active_weather_threats.append(threat_payload)
            else:
                historical_baseline_risks.append(threat_payload)

        # Sort both lists by highest probability descending
        active_weather_threats = sorted(active_weather_threats, key=lambda x: x["probability"], reverse=True)
        historical_baseline_risks = sorted(historical_baseline_risks, key=lambda x: x["probability"], reverse=True)

        return {
            "ward": ward,
            "timestamp": datetime.datetime.now().isoformat(),
            "environmental_inputs": {
                "temperature": temperature,
                "humidity": humidity,
                "rainfall": rainfall,
                "water_level": water_level,
                "is_monsoon": bool(is_monsoon)
            },
            "active_weather_threats": active_weather_threats,
            "historical_baseline_risks": historical_baseline_risks
        }
