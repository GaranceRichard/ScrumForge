from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Nécessite un JWT valide
def home_api(request):
    return Response({"message": "Bienvenue sur l'API !", "user": request.user.username})


class LogoutView(APIView):
    """Gère la déconnexion en invalidant le refresh token"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist le token pour empêcher son utilisation future

            return Response({"message": "Déconnexion réussie."}, status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response({"error": "Token invalide ou déjà expiré."}, status=status.HTTP_400_BAD_REQUEST)

User = get_user_model()
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
