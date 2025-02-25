from django.urls import path
from .views import (
    CertificationListCreateView,
    CertificationDetailView,
    CertificationCompetencyUpdateView,
    CompetencyListCreateView,
    CompetencyDetailView,
)

urlpatterns = [
    # Endpoints pour Certifications (accessibles via /certifications/…)
    path('', CertificationListCreateView.as_view(), name='certification-list-create'),
    path('<int:pk>/', CertificationDetailView.as_view(), name='certification-detail'),
    path('<int:certification_id>/competencies/', CertificationCompetencyUpdateView.as_view(), name='certification-competency-update'),

    # Endpoints pour Compétences
    path('competencies/', CompetencyListCreateView.as_view(), name='competency-list-create'),
    path('competencies/<int:pk>/', CompetencyDetailView.as_view(), name='competency-detail'),
]
