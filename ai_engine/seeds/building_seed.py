import random
import uuid
from datetime import date, timedelta

WARDS = [
    "Naupada-Kopri", "Uthalsar", "Wagle Estate", "Lokmanya-Savarkar Nagar",
    "Vartak Nagar", "Majiwada-Manpada", "Kalwa", "Mumbra", "Diva"
]

def generate_buildings(count=1000):
    buildings = []
    for i in range(count):
        year_built = random.randint(1950, 2025)
        age = 2026 - year_built
        
        if age > 40:
            condition = random.choices(["Poor", "Dilapidated", "Fair"], weights=[40, 40, 20])[0]
            risk_level = random.choices(["C1", "C2A", "C2B", "C3"], weights=[20, 30, 30, 20])[0]
        elif age > 20:
            condition = random.choices(["Fair", "Good", "Poor"], weights=[60, 30, 10])[0]
            risk_level = random.choices(["Safe", "C3", "C2B"], weights=[70, 20, 10])[0]
        else:
            condition = random.choices(["Good", "Fair"], weights=[90, 10])[0]
            risk_level = "Safe"
            
        if risk_level == "C1":
            action = "Demolish"
        elif risk_level in ["C2A", "C2B"]:
            action = "Evacuate" if risk_level == "C2A" else "Repair"
        elif risk_level == "C3":
            action = "Repair"
        else:
            action = "Monitor"

        inspection_date = date(2018, 1, 1) + timedelta(days=random.randint(0, 3000))
        if inspection_date.year < year_built:
            inspection_date = date(year_built, 1, 1) + timedelta(days=random.randint(1, 365))
            
        buildings.append({
            "building_id": str(uuid.uuid4()),
            "building_name": f"Building {i+1} CHS",
            "ward": random.choice(WARDS),
            "area": "Sector " + str(random.randint(1, 20)),
            "year_built": year_built,
            "inspection_date": inspection_date.isoformat(),
            "condition": condition,
            "risk_level": risk_level,
            "recommended_action": action
        })
    return buildings
