from django.contrib import admin
from django.urls import path, include
from authentication.views import home_api  # Vue d'accueil si connecté

urlpatterns = [
    path('', home_api, name='home_api'),  # API qui remplace l'ancienne vue inutile
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('certifications/', include('certifications.urls')),
    path('dashboard/', include('dashboard.urls')),
]
