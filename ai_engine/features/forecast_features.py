from datetime import datetime

class ForecastFeatureEngineer:
    """
    Transforms time-series incident data into temporal features for ARIMA/Prophet models.
    """

    @staticmethod
    def extract_temporal_features(target_date_str):
        """
        Extracts temporal and seasonal encodings for time-series forecasting.
        """
        target = datetime.fromisoformat(target_date_str)
        month = target.month
        
        # Simple one-hot encoding for seasons
        season = [0, 0, 0] # [Monsoon, Summer, Winter]
        if month in [6, 7, 8, 9]:
            season[0] = 1
        elif month in [3, 4, 5]:
            season[1] = 1
        else:
            season[2] = 1
            
        features = {
            "month_of_year": month,
            "is_monsoon": season[0],
            "is_summer": season[1],
            "is_winter": season[2],
            "year_index": target.year - 2018 # Assuming 2018 is baseline
        }
        
        return features
