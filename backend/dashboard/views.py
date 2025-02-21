from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]  # Permet seulement aux utilisateurs authentifiés d'accéder

    def get(self, request, *args, **kwargs):
        return Response({"message": "Bienvenue sur le Dashboard"}, status=200)
