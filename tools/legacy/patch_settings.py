with open('dmd_project/urls.py', 'r') as f:
    data = f.read()

if "path('api/ai/', include('ai_api.urls'))" not in data:
    data = data.replace(
        "from django.urls import path, include",
        "from django.urls import path, include"
    )
    if "from django.urls import path, include" not in data:
        data = data.replace("from django.urls import path", "from django.urls import path, include")
    
    data = data.replace(
        "urlpatterns = [",
        "urlpatterns = [\n    path('api/ai/', include('ai_api.urls')),"
    )

    with open('dmd_project/urls.py', 'w') as f:
        f.write(data)
