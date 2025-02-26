from authentication.serializers import HomeSerializer, LogoutSerializer, ResetPasswordSerializer, ResetPasswordResponseSerializer
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema


User = get_user_model()

# ==========================
# 🏠 Home API
# ==========================
@extend_schema(responses=HomeSerializer)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def home_api(request):
    """Retourne un message de bienvenue et le nom de l'utilisateur connecté"""
    return Response({"message": "Bienvenue sur l'API !", "user": request.user.username})

# ==========================
# 🔐 Authentication APIs
# ==========================
@extend_schema(
    request=None,
    responses={205: LogoutSerializer}  # 🔥 Correction : Indiquer clairement le serializer
)
class LogoutView(APIView):
    """Déconnexion d'un utilisateur en blacklistant son refresh token"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Le token de déconnexion est requis."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Déconnexion réussie."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Token invalide ou déjà expiré."}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=ResetPasswordSerializer,
    responses={200: ResetPasswordResponseSerializer, 404: {"error": "Aucun utilisateur trouvé"}}
)
class ResetPasswordView(APIView):
    """Génération d'un nouveau mot de passe pour un utilisateur"""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
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
            "username": user.username,
        }
        if settings.DEBUG:
            response_data["new_password"] = new_password

        return Response(response_data, status=status.HTTP_200_OK)

def social_auth_redirect(request):
    # Logique après l'authentification réussie
    user = request.user
    login(request, user)
    return redirect('home')  # Remplace par la vue que tu veux rediriger
