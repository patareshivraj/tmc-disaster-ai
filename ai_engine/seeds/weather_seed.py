import random
import uuid
from datetime import date, timedelta

WARDS = [
    "Naupada-Kopri", "Uthalsar", "Wagle Estate", "Lokmanya-Savarkar Nagar",
    "Vartak Nagar", "Majiwada-Manpada", "Kalwa", "Mumbra", "Diva"
]

def generate_weather(count=5000):
    weather = []
    start_date = date(2018, 1, 1)
    
    for _ in range(count):
        current_date = start_date + timedelta(days=random.randint(0, 3280))
        ward = random.choice(WARDS)
        month = current_date.month
        
        is_monsoon = month in [6, 7, 8, 9]
        is_summer = month in [3, 4, 5]
        
        if is_monsoon:
            rainfall = round(random.uniform(0.0, 250.0), 1)
            temp = round(random.uniform(24.0, 32.0), 1)
            humidity = round(random.uniform(70.0, 100.0), 1)
            water_level = round(random.uniform(2.0, 6.0), 1)
        elif is_summer:
            rainfall = round(random.uniform(0.0, 10.0), 1)
            temp = round(random.uniform(32.0, 42.0), 1)
            humidity = round(random.uniform(30.0, 60.0), 1)
            water_level = round(random.uniform(0.5, 2.0), 1)
        else:
            rainfall = round(random.uniform(0.0, 5.0), 1)
            temp = round(random.uniform(18.0, 30.0), 1)
            humidity = round(random.uniform(40.0, 70.0), 1)
            water_level = round(random.uniform(1.0, 3.0), 1)
            
        alert = "None"
        if rainfall > 150: alert = "Red"
        elif rainfall > 100: alert = "Orange"
        elif rainfall > 50: alert = "Yellow"
        
        weather.append({
            "date": current_date.isoformat(),
            "ward": ward,
            "rainfall_mm": rainfall,
            "temperature": temp,
            "humidity": humidity,
            "water_level_m": water_level,
            "alert_level": alert
        })
    return weather
