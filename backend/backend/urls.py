from django.contrib import admin
from django.urls import path, include
from authentication.views import home  # Vue d'accueil si connecté

urlpatterns = [
    path('', home, name='home'),  # Page d'accueil protégée
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),  # Routes d'authentification
    path('certifications/', include('certifications.urls')),  # Gérer les certifications
    path('dashboard/', include('dashboard.urls')),  # Accès au dashboard
]
