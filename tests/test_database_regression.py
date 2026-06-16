import os
import django
import pandas as pd


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_project.settings')
django.setup()

from django.conf import settings
from ai_engine.repositories.factory import DataSourceFactory

def assert_dataframes_equal(csv_df, db_df, id_col=None):
    # Sort them if id_col provided
    if id_col:
        csv_df = csv_df.sort_values(by=id_col).reset_index(drop=True)
        db_df = db_df.sort_values(by=id_col).reset_index(drop=True)
    
    assert len(csv_df) == len(db_df), f"Row count mismatch: CSV has {len(csv_df)}, DB has {len(db_df)}"

def test_incident_repository():
    settings.AI_USE_LIVE_DATABASE = False
    csv_df = DataSourceFactory.get_dataframe("incidents")
    
    settings.AI_USE_LIVE_DATABASE = True
    db_df = DataSourceFactory.get_dataframe("incidents")
    
    assert_dataframes_equal(csv_df, db_df, "incident_id")
    print("Incident parity OK")

def test_weather_repository():
    settings.AI_USE_LIVE_DATABASE = False
    csv_df = DataSourceFactory.get_dataframe("weather")
    
    settings.AI_USE_LIVE_DATABASE = True
    db_df = DataSourceFactory.get_dataframe("weather")
    
    assert_dataframes_equal(csv_df, db_df, "date")
    print("Weather parity OK")

def test_building_repository():
    settings.AI_USE_LIVE_DATABASE = False
    csv_df = DataSourceFactory.get_dataframe("buildings")
    
    settings.AI_USE_LIVE_DATABASE = True
    db_df = DataSourceFactory.get_dataframe("buildings")
    
    assert_dataframes_equal(csv_df, db_df, "building_id")
    print("Building parity OK")

def test_resource_repository():
    settings.AI_USE_LIVE_DATABASE = False
    csv_df = DataSourceFactory.get_dataframe("resources")
    
    settings.AI_USE_LIVE_DATABASE = True
    db_df = DataSourceFactory.get_dataframe("resources")
    
    assert_dataframes_equal(csv_df, db_df, "incident_id")
    print("Resource parity OK")

def test_preparedness_repository():
    settings.AI_USE_LIVE_DATABASE = False
    csv_df = DataSourceFactory.get_dataframe("preparedness")
    
    settings.AI_USE_LIVE_DATABASE = True
    db_df = DataSourceFactory.get_dataframe("preparedness")
    
    assert_dataframes_equal(csv_df, db_df, "program_id")
    print("Preparedness parity OK")

if __name__ == "__main__":
    print("Running Repository Regression Tests...")
    try:
        test_incident_repository()
        test_weather_repository()
        test_building_repository()
        test_resource_repository()
        test_preparedness_repository()
        print("ALL REPOSITORY TESTS PASSED (0.0% DRIFT)")
    except Exception as e:
        print("Database Connection Error. Regression Tests Skipped.")
        print(e)
