with open('dmd_project/settings.py', 'r') as f:
    data = f.read()

data = data.replace("'ai_api',", "'ai_api',\n    'ai_monitoring',")

with open('dmd_project/settings.py', 'w') as f:
    f.write(data)
