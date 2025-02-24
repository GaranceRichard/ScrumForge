from authentication.serializers import UserSerializer, HomeSerializer, LogoutSerializer, ResetPasswordSerializer, ResetPasswordResponseSerializer
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404, redirect
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


class RegisterView(generics.CreateAPIView):
    """Inscription d'un nouvel utilisateur"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

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

# ==========================
# 👥 User Management APIs
# ==========================
class UserListView(generics.ListAPIView):
    """Liste tous les utilisateurs (réservé aux admins)"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

@extend_schema(
    request=UserSerializer,
    responses={
        200: UserSerializer,
        400: {"error": "L'ID de l'utilisateur est requis"},
        403: {"error": "Vous devez être administrateur pour modifier un utilisateur."}
    }
)
class UserUpdateView(APIView):
    """Modification d'un utilisateur par un administrateur uniquement"""

    permission_classes = [IsAdminUser]  # ✅ Seuls les admins peuvent modifier les utilisateurs

    def patch(self, request, user_id=None):
        if not user_id:
            return Response({"error": "L'ID de l'utilisateur est requis."}, status=status.HTTP_400_BAD_REQUEST)

        # 🔥 Vérification stricte : seuls les admins peuvent modifier un utilisateur
        if not request.user.is_staff:
            return Response(
                {"error": "Accès interdit. Seuls les administrateurs peuvent modifier un utilisateur."},
                status=status.HTTP_403_FORBIDDEN
            )

        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=UserSerializer,
    responses={
        200: UserSerializer,
        403: {"error": "Vous ne pouvez modifier que votre propre compte."}
    }
)
class UserSelfUpdateView(generics.UpdateAPIView):
    """Permet à un utilisateur de modifier son propre profil"""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

@extend_schema(responses={204: None, 400: {"error": "L'ID de l'utilisateur est requis"}, 403: {"error": "Impossible de supprimer un superutilisateur"}})
class UserDeleteView(APIView):
    """Suppression d'un utilisateur par un administrateur"""

    permission_classes = [IsAdminUser]

    def delete(self, request, user_id=None):
        if not user_id:
            return Response({"error": "L'ID de l'utilisateur est requis."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)

        if user.is_superuser:
            return Response({"error": "Impossible de supprimer un superutilisateur."}, status=status.HTTP_403_FORBIDDEN)

        user.delete()
        return Response({"message": "Utilisateur supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)


def social_auth_redirect(request):
    # Logique après l'authentification réussie
    user = request.user
    login(request, user)
    return redirect('home')  # Remplace par la vue que tu veux rediriger
