import random
import uuid
from datetime import date, timedelta

WARDS = [
    "Naupada-Kopri", "Uthalsar", "Wagle Estate", "Lokmanya-Savarkar Nagar",
    "Vartak Nagar", "Majiwada-Manpada", "Kalwa", "Mumbra", "Diva"
]

def generate_preparedness(count=500):
    programs = []
    start_date = date(2018, 1, 1)
    
    types = ["Mock Drill", "Citizen Awareness", "School Safety", "Hospital Preparedness"]
    
    for _ in range(count):
        current_date = start_date + timedelta(days=random.randint(0, 3280))
        programs.append({
            "program_id": str(uuid.uuid4()),
            "ward": random.choice(WARDS),
            "program_type": random.choice(types),
            "date": current_date.isoformat(),
            "participants": random.randint(50, 1000),
            "outcome": random.choices(["Successful", "Excellent", "Needs Improvement"], weights=[60, 30, 10])[0]
        })
    return programs
