with open('dmd_project/settings.py', 'r') as f:
    data = f.read()

import re
db_pattern = re.compile(r"DATABASES = \{.*?\n\}", re.DOTALL)
sqlite_db = """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""
data = db_pattern.sub(sqlite_db, data)

with open('dmd_project/settings.py', 'w') as f:
    f.write(data)
