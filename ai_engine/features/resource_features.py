class ResourceFeatureEngineer:
    """
    Transforms incoming incident alerts into feature vectors for Resource ML matching.
    """
    
    SEVERITY_MAP = {
        "Minor": 1,
        "Moderate": 2,
        "Major": 3,
        "Critical": 4
    }

    @staticmethod
    def extract_features(incident, historical_resources=None):
        """
        Builds the AI feature vector for Resource Recommendation.
        """
        severity_score = ResourceFeatureEngineer.SEVERITY_MAP.get(incident.get('severity', 'Minor'), 1)
        
        features = {
            "incident_type": incident.get('incident_type'),
            "severity_encoded": severity_score,
            "ward": incident.get('ward'),
            "is_major_disaster": 1 if severity_score >= 3 else 0,
            "population_impact_log": incident.get('affected_population', 0), # Normally log-scaled
        }
        
        # If we have historical averages for this type/severity, append them
        if historical_resources:
            # Logic to compute historical_resource_utilization_rate goes here
            features['historical_utilization_rate'] = 1.0 
            
        return features
