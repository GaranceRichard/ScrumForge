from django.contrib import admin
from django.urls import path, include
from authentication.views import home_api  # Vue d'accueil si connecté
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('', home_api, name='home_api'),  # API qui remplace l'ancienne vue inutile
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('user-management/', include('user_management.urls')),
    path('certifications/', include('certifications.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]
