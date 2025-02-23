from django.conf import settings  # Importer les settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer



User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Nécessite un JWT valide
def home_api(request):
    return Response({"message": "Bienvenue sur l'API !", "user": request.user.username})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Le token de déconnexion est requis."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Déconnexion réussie."}, status=status.HTTP_205_RESET_CONTENT)

        except Exception:
            return Response(
                {"error": "Token invalide ou déjà expiré."},
                status=status.HTTP_400_BAD_REQUEST
            )

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class ResetPasswordView(APIView):
    """Permet de récupérer le username et générer un mot de passe aléatoire"""
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "L'email est requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Aucun utilisateur trouvé avec cet email."}, status=status.HTTP_404_NOT_FOUND)

        new_password = get_random_string(length=12)
        user.set_password(new_password)
        user.save()

        send_mail(
            subject="Réinitialisation de votre mot de passe",
            message=f"Bonjour {user.username}, votre nouveau mot de passe est : {new_password}",
            from_email="no-reply@scrumforge.com",
            recipient_list=[user.email],
            fail_silently=False,
        )

        response_data = {
            "message": "Un nouveau mot de passe a été envoyé.",
            "username": user.username
        }

        if settings.DEBUG:  # 🔥 Vérifie bien que DEBUG=True
            response_data["new_password"] = new_password

        return Response(response_data, status=status.HTTP_200_OK)
