from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .serializers import DashboardSerializer  # 🔹 Import du serializer

@extend_schema(responses=DashboardSerializer)  # 🔹 Ajout du schema pour DRF Spectacular
class DashboardView(APIView):
    """Vue du Dashboard (nécessite une authentification)"""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({"message": "Bienvenue sur le Dashboard"}, status=200)
