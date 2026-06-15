import os
import csv
import json
from ai_engine.seeds.team_seed import generate_teams
from ai_engine.seeds.building_seed import generate_buildings
from ai_engine.seeds.weather_seed import generate_weather
from ai_engine.seeds.incident_seed import generate_incidents
from ai_engine.seeds.resource_seed import generate_resources
from ai_engine.seeds.preparedness_seed import generate_preparedness

OUTPUT_DIR = "generated_data"

def export_data(filename, data):
    if not data: return
    
    # JSON
    with open(os.path.join(OUTPUT_DIR, f"{filename}.json"), 'w') as f:
        json.dump(data, f, indent=4)
        
    # CSV
    keys = data[0].keys()
    with open(os.path.join(OUTPUT_DIR, f"{filename}.csv"), 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
        
def validate_weather(data):
    for r in data:
        assert r['rainfall_mm'] >= 0, "Negative rainfall"
        assert r['temperature'] >= 0, "Negative temperature"

def validate_incidents(data):
    for r in data:
        assert r['affected_population'] >= 0, "Negative population"
        assert r['response_time_minutes'] / 60 <= r['resolution_time_hours'], "Response time > Resolution time"
        if r['severity'] == "Critical":
            assert r['financial_loss'] > 0, "Critical incident with 0 loss"

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Starting Synthetic Data Generation...")
    
    # 1. Teams
    teams = generate_teams(random.randint(30, 50))
    print(f"Generated {len(teams)} response teams.")
    export_data("teams", teams)
    
    # 2. Buildings
    buildings = generate_buildings(1000)
    print(f"Generated {len(buildings)} buildings.")
    export_data("buildings", buildings)
    
    # 3. Weather
    weather = generate_weather(5500)
    validate_weather(weather)
    print(f"Generated {len(weather)} weather records.")
    export_data("weather", weather)
    
    # 4. Incidents
    incidents = generate_incidents(2500)
    validate_incidents(incidents)
    print(f"Generated {len(incidents)} incidents.")
    export_data("incidents", incidents)
    
    # 5. Resources
    resources = generate_resources(incidents)
    print(f"Generated {len(resources)} resource records.")
    export_data("resources", resources)
    
    # 6. Preparedness
    programs = generate_preparedness(500)
    print(f"Generated {len(programs)} preparedness programs.")
    export_data("preparedness", programs)
    
    print("Generation complete! All files saved in 'generated_data/' directory.")

if __name__ == "__main__":
    import random
    random.seed(42) # Repeatable randomness
    main()
