from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Certification, Competency, CertificationCompetency
from .serializers import (
    CertificationSerializer,
    CompetencySerializer,
    CertificationCompetencyUpdateSerializer
)

class CertificationListCreateView(generics.ListCreateAPIView):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer

    def get_permissions(self):
        # Seuls les admins peuvent créer, sinon l'utilisateur doit être authentifié.
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class CertificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer

    def get_permissions(self):
        # La mise à jour et la suppression sont réservées aux admins, sinon authentification requise.
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class CompetencyListCreateView(generics.ListCreateAPIView):
    queryset = Competency.objects.all()
    serializer_class = CompetencySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

@extend_schema_view(
    patch=extend_schema(operation_id="competency_partial_update"),
    put=extend_schema(operation_id="competency_update")
)
class CompetencyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Competency.objects.all()
    serializer_class = CompetencySerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

@extend_schema(
    request=CertificationCompetencyUpdateSerializer,
    responses={200: {"type": "object", "properties": {"message": {"type": "string"}}}}
)
class CertificationCompetencyUpdateView(APIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CertificationCompetencyUpdateSerializer

    def put(self, request, certification_id):
        serializer = CertificationCompetencyUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        competency_ids = serializer.validated_data.get("competency_ids", [])
        # Récupération de la certification
        try:
            cert = Certification.objects.get(id=certification_id)
        except Certification.DoesNotExist:
            return Response({"error": "Certification introuvable."}, status=status.HTTP_404_NOT_FOUND)
        # Supprime les associations existantes et recrée
        CertificationCompetency.objects.filter(certification=cert).delete()
        for comp_id in competency_ids:
            try:
                comp = Competency.objects.get(id=comp_id)
                CertificationCompetency.objects.create(certification=cert, competency=comp)
            except Competency.DoesNotExist:
                continue
        return Response({"message": "Associations mises à jour avec succès."}, status=status.HTTP_200_OK)
