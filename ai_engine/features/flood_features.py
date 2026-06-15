import pandas as pd
import numpy as np

def create_flood_features(weather_csv="generated_data/weather.csv", incidents_csv="generated_data/incidents.csv"):
    """
    Consumes raw weather and incident data to produce ML-ready flood features.
    """
    # 1. Load Data
    weather_df = pd.read_csv(weather_csv)
    weather_df['date'] = pd.to_datetime(weather_df['date'])
    weather_df = weather_df.sort_values(by=['ward', 'date']).reset_index(drop=True)
    
    incidents_df = pd.read_csv(incidents_csv)
    incidents_df['incident_date'] = pd.to_datetime(incidents_df['incident_date'])
    
    # Filter for floods
    floods = incidents_df[incidents_df['incident_type'].isin(['Flood', 'Water Logging'])]
    floods = floods.groupby(['ward', 'incident_date']).size().reset_index(name='flood_count')
    
    # 2. Merge Weather & Incidents
    df = pd.merge(weather_df, floods, left_on=['ward', 'date'], right_on=['ward', 'incident_date'], how='left')
    df['has_flood'] = (df['flood_count'] > 0).astype(int)
    
    # 3. Create Rolling Features (3-day and 7-day average rainfall)
    df['3_day_avg_rainfall'] = df.groupby('ward')['rainfall_mm'].transform(lambda x: x.rolling(window=3, min_periods=1).mean())
    df['7_day_avg_rainfall'] = df.groupby('ward')['rainfall_mm'].transform(lambda x: x.rolling(window=7, min_periods=1).mean())
    
    # 4. Previous Flood Count (cumulative count up to that date)
    df['previous_flood_count'] = df.groupby('ward')['has_flood'].cumsum() - df['has_flood']
    
    # 5. Extract Temporal Features
    df['month'] = df['date'].dt.month
    df['is_monsoon'] = df['month'].isin([6, 7, 8, 9]).astype(int)
    
    # Clean up and order columns
    features = ['date', 'ward', 'rainfall_mm', 'humidity', 'water_level_m', 'temperature', 
                '3_day_avg_rainfall', '7_day_avg_rainfall', 'previous_flood_count', 'is_monsoon', 'has_flood']
    
    return df[features]
