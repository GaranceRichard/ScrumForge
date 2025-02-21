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
        new_password = get_random_string(length=12)  # Générer un mot de passe aléatoire
        user.set_password(new_password)
        user.save()
        # Envoyer un email simulé ou réel selon l'environnement
        send_mail(
            subject="Réinitialisation de votre mot de passe",
            message=f"Bonjour {user.username},\n\nVotre nouveau mot de passe est : {new_password}\n\nVeuillez le modifier après connexion.",
            from_email="no-reply@scrumforge.com",
            recipient_list=[user.email],
            fail_silently=False,
        )
        # Construire la réponse JSON
        response_data = {
            "message": "Un nouveau mot de passe a été envoyé à votre adresse email.",
            "username": user.username
        }
        # 🔹 Si on est en mode DEBUG, on inclut le mot de passe dans la réponse
        if settings.DEBUG:
            response_data["new_password"] = new_password

        return Response(response_data, status=status.HTTP_200_OK)
