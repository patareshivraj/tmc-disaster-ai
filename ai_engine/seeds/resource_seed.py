import random
import uuid
import json

def generate_resources(incidents):
    resources = []
    
    for inc in incidents:
        itype = inc['incident_type']
        sev = inc['severity']
        
        boats = 0
        pumps = 0
        vehicles = 1
        equip = []
        
        if sev in ["Major", "Critical"]:
            vehicles += random.randint(2, 5)
            
        if itype == "Flood" or itype == "Water Logging":
            boats = random.randint(1, 5) if sev in ["Major", "Critical"] else random.randint(0, 1)
            pumps = random.randint(2, 10) if sev in ["Major", "Critical"] else random.randint(0, 2)
            equip.append("Life Jackets")
            equip.append("Ropes")
            
        elif itype == "Fire":
            vehicles = random.randint(3, 8) if sev in ["Major", "Critical"] else random.randint(1, 2)
            equip.append("Fire Hoses")
            equip.append("Breathing Apparatus")
            
        elif itype == "Tree Fall":
            equip.append("Chainsaws")
            vehicles += 1
            
        elif itype == "Gas Leakage":
            equip.append("Safety Kits")
            equip.append("Gas Detectors")
            
        elif itype == "Building Emergency":
            equip.append("Earthmovers")
            vehicles += 2
            
        fuel = round((vehicles * 15.5) + (boats * 20.0) + (pumps * 5.5), 2)
        
        resources.append({
            "resource_id": str(uuid.uuid4()),
            "incident_id": inc['incident_id'],
            "boats_used": boats,
            "vehicles_used": vehicles,
            "pumps_used": pumps,
            "equipment_used": json.dumps(equip),
            "fuel_consumed": fuel
        })
    return resources
