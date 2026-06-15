from datetime import datetime

class BuildingFeatureEngineer:
    """
    Transforms raw building inspection logs into AI-ready vectors for safety classification.
    """
    
    CONDITION_MAP = {
        "Good": 1,
        "Fair": 2,
        "Poor": 3,
        "Dilapidated": 4
    }
    
    RISK_MAP = {
        "Safe": 0,
        "C3": 1,
        "C2B": 2,
        "C2A": 3,
        "C1": 4
    }

    @staticmethod
    def extract_features(building_record, current_year=2026):
        """
        Converts building inspection string logic into mathematical tensors.
        """
        year_built = int(building_record['year_built'])
        inspection_date = datetime.fromisoformat(building_record['inspection_date'])
        
        features = {
            "building_id": building_record['building_id'],
            "building_age": current_year - year_built,
            "condition_encoded": BuildingFeatureEngineer.CONDITION_MAP.get(building_record['condition'], 2),
            "historical_risk_encoded": BuildingFeatureEngineer.RISK_MAP.get(building_record['risk_level'], 0),
            "years_since_inspection": current_year - inspection_date.year,
            "is_critical_age": 1 if (current_year - year_built) > 40 else 0
        }
        
        return features
