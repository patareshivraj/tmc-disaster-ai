import sys
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_project.settings')
django.setup()

from ai_engine.repositories.factory import DataSourceFactory
try:
    df = DataSourceFactory.get_dataframe("buildings")
    print(df.head())
except Exception as e:
    print("ERROR loading buildings:", e)
