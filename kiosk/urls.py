from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # First check for config/
    path('config/', include('serve_config.urls')),
    # Then everything else
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
]
