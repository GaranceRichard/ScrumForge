from django.urls import path
from .views import certification_list  # Importe une vue (à créer si nécessaire)

urlpatterns = [
    path('', certification_list, name='certifications'),
]
