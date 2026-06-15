import random
import uuid
from datetime import date, timedelta

WARDS = [
    "Naupada-Kopri", "Uthalsar", "Wagle Estate", "Lokmanya-Savarkar Nagar",
    "Vartak Nagar", "Majiwada-Manpada", "Kalwa", "Mumbra", "Diva"
]

def generate_incidents(count=2500):
    incidents = []
    start_date = date(2018, 1, 1)
    
    types_weights = {
        "Flood": 35, "Tree Fall": 20, "Fire": 15, "Road Accident": 10,
        "Building Emergency": 8, "Gas Leakage": 5, "Heat Wave": 3,
        "Electrical Hazard": 2, "Landslide": 2
    }
    types = list(types_weights.keys())
    weights = list(types_weights.values())
    
    for _ in range(count):
        itype = random.choices(types, weights=weights)[0]
        
        # Enforce rules
        month = random.randint(1, 12)
        if itype in ["Flood", "Tree Fall"]:
            month = random.choices([6, 7, 8, 9], weights=[20, 30, 30, 20])[0]
        elif itype == "Heat Wave":
            month = random.choice([4, 5])
            
        year = random.randint(2018, 2026)
        day = random.randint(1, 28)
        incident_date = date(year, month, day)
        
        ward = random.choice(WARDS)
        if itype == "Landslide":
            ward = random.choice(["Mumbra", "Diva", "Kalwa"])
            
        severity = random.choices(["Minor", "Moderate", "Major", "Critical"], weights=[40, 30, 20, 10])[0]
        
        deaths = 0
        injuries = random.randint(0, 5) if severity in ["Minor", "Moderate"] else random.randint(2, 20)
        loss = round(random.uniform(1000, 50000), 2)
        
        if severity == "Critical":
            deaths = random.randint(0, 5)
            loss = round(random.uniform(100000, 1000000), 2)
            
        response_m = random.randint(5, 60)
        res_h = random.randint(1, 72)
        if response_m / 60 >= res_h:
            res_h = int(response_m / 60) + 1
            
        incidents.append({
            "incident_id": str(uuid.uuid4()),
            "incident_date": incident_date.isoformat(),
            "ward": ward,
            "area": "Locality " + str(random.randint(1, 50)),
            "incident_type": itype,
            "severity": severity,
            "affected_population": random.randint(0, 500) if severity in ["Major", "Critical"] else random.randint(0, 20),
            "injuries": injuries,
            "deaths": deaths,
            "financial_loss": loss,
            "response_time_minutes": response_m,
            "resolution_time_hours": res_h,
            "status": "Resolved"
        })
    return incidents
