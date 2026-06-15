from datetime import datetime

class RiskFeatureEngineer:
    """
    Transforms aggregated historical data into a normalized risk matrix for TMC Wards.
    """
    
    @staticmethod
    def calculate_incident_density(incidents, target_ward, months_back=12):
        """
        Calculates incident density for the given ward over the last N months.
        """
        # In a real system, filter by date relative to 'now'
        count = sum(1 for i in incidents if i['ward'] == target_ward)
        return count / months_back

    @staticmethod
    def calculate_preparedness_score(preparedness_records, target_ward):
        """
        Calculates a preparedness safety score based on drills and awareness.
        """
        ward_programs = [p for p in preparedness_records if p['ward'] == target_ward]
        score = 0
        for p in ward_programs:
            if p['outcome'] == "Excellent":
                score += 1.5
            elif p['outcome'] == "Successful":
                score += 1.0
            else:
                score += 0.5
        return score

    @staticmethod
    def extract_features(target_ward, incidents, preparedness):
        """
        Builds the AI feature vector for Ward Risk Analysis.
        """
        ward_incidents = [i for i in incidents if i['ward'] == target_ward]
        
        # Calculate severe incident ratio
        severe_count = sum(1 for i in ward_incidents if i['severity'] in ["Major", "Critical"])
        severe_ratio = severe_count / len(ward_incidents) if ward_incidents else 0.0
        
        features = {
            "ward": target_ward,
            "incident_density": RiskFeatureEngineer.calculate_incident_density(incidents, target_ward),
            "severe_incident_ratio": round(severe_ratio, 3),
            "preparedness_score": RiskFeatureEngineer.calculate_preparedness_score(preparedness, target_ward),
            "response_efficiency_score": 0.0 # Placeholder for response time logic
        }
        
        return features
