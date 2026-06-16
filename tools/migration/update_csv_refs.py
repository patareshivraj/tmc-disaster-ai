import glob
import os
import re

files_to_update = glob.glob('ai_engine/training/*.py')
files_to_update += glob.glob('ai_engine/models/*.py')
files_to_update += glob.glob('ai_engine/features/*.py')
files_to_update += glob.glob('ai_engine/chatbot/*.py')

import_statement = "from ai_engine.repositories.factory import DataSourceFactory"

for fpath in files_to_update:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'pd.read_csv' in content:
        if import_statement not in content:
            # Find first import and insert after it
            content = re.sub(r'^(import .*?\n)', r'\g<1>' + import_statement + '\n', content, count=1)
        
        # Replace occurrences
        content = re.sub(r'pd\.read_csv\(.*?incidents\.csv["\']\)', 'DataSourceFactory.get_dataframe("incidents")', content)
        content = re.sub(r'pd\.read_csv\(.*?buildings\.csv["\']\)', 'DataSourceFactory.get_dataframe("buildings")', content)
        content = re.sub(r'pd\.read_csv\(.*?preparedness\.csv["\']\)', 'DataSourceFactory.get_dataframe("preparedness")', content)
        content = re.sub(r'pd\.read_csv\(.*?weather\.csv["\']\)', 'DataSourceFactory.get_dataframe("weather")', content)
        content = re.sub(r'pd\.read_csv\(.*?resources\.csv["\']\)', 'DataSourceFactory.get_dataframe("resources")', content)
        
        # Fix the remaining dynamic arguments in flood_features if any
        content = re.sub(r'pd\.read_csv\(weather_csv\)', 'DataSourceFactory.get_dataframe("weather")', content)
        content = re.sub(r'pd\.read_csv\(incidents_csv\)', 'DataSourceFactory.get_dataframe("incidents")', content)
        
        # Fix dynamic arg in building_advisor_model
        content = re.sub(r'pd\.read_csv\(data_path\)', 'DataSourceFactory.get_dataframe("buildings")', content)

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated {fpath}")

