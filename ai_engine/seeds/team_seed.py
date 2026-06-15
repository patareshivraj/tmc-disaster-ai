import random
import uuid

WARDS = [
    "Naupada-Kopri", "Uthalsar", "Wagle Estate", "Lokmanya-Savarkar Nagar",
    "Vartak Nagar", "Majiwada-Manpada", "Kalwa", "Mumbra", "Diva"
]

NAMES = ["Rajesh", "Amit", "Suresh", "Vijay", "Anil", "Prakash", "Sanjay", "Ramesh", "Deepak", "Ravi"]
SURNAMES = ["Patil", "Deshmukh", "Jadhav", "Shinde", "Pawar", "Gaikwad", "Kadam", "Kale", "Kulkarni", "Joshi"]

def generate_teams(count=40):
    teams = []
    for i in range(count):
        ward = random.choice(WARDS)
        teams.append({
            "team_id": str(uuid.uuid4()),
            "team_name": f"TDRF Unit {i+1} - {ward}",
            "ward": ward,
            "leader_name": f"{random.choice(NAMES)} {random.choice(SURNAMES)}",
            "member_count": random.randint(5, 25),
            "vehicles": random.randint(1, 5),
            "boats": random.randint(0, 3) if ward in ["Mumbra", "Kalwa", "Diva"] else random.randint(0, 1),
            "equipment_count": random.randint(20, 100),
            "availability": random.choices(["Available", "Deployed", "Maintenance"], weights=[80, 15, 5])[0]
        })
    return teams
