from authentication.serializers import UserSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

User = get_user_model()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def home_api(request):
    """Retourne un message de bienvenue et le nom de l'utilisateur connecté"""
    return Response({"message": "Bienvenue sur l'API !", "user": request.user.username})


class LogoutView(APIView):
    """Déconnexion d'un utilisateur en blacklistant son refresh token"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"error": "Le token de déconnexion est requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Déconnexion réussie."},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception:
            return Response(
                {"error": "Token invalide ou déjà expiré."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RegisterView(generics.CreateAPIView):
    """Inscription d'un nouvel utilisateur"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ResetPasswordView(APIView):
    """Génération d'un nouveau mot de passe pour un utilisateur"""

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "L'email est requis."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Aucun utilisateur trouvé avec cet email."},
                status=status.HTTP_404_NOT_FOUND,
            )

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


class UserListView(generics.ListAPIView):
    """Liste tous les utilisateurs (réservé aux admins)"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserUpdateView(APIView):
    """Modification d'un utilisateur par un admin (supporte ID en URL et JSON)"""

    permission_classes = [IsAdminUser]

    def patch(self, request, user_id=None):
        """Mise à jour partielle d'un utilisateur avec ID en URL ou JSON"""
        user_id = user_id or request.data.get("user_id")  # 🔥 Récupère l'ID en URL ou JSON

        if not user_id:
            return Response({"error": "L'ID de l'utilisateur est requis."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSelfUpdateView(generics.UpdateAPIView):
    """Permet à un utilisateur de modifier son propre username ou email"""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # 🔥 Récupération directe de l'utilisateur connecté


class UserDeleteView(APIView):
    """Suppression d'un utilisateur par un admin (supporte ID en URL et JSON)"""

    permission_classes = [IsAdminUser]

    def delete(self, request, user_id=None):
        """Supprime un utilisateur en passant l'ID dans l'URL ou le JSON"""
        user_id = user_id or request.data.get("user_id")  # 🔥 Récupère l'ID en URL ou JSON

        if not user_id:
            return Response({"error": "L'ID de l'utilisateur est requis."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)

        if user.is_superuser:
            return Response(
                {"error": "Impossible de supprimer un superutilisateur."},
                status=status.HTTP_403_FORBIDDEN,
            )

        user.delete()
        return Response({"message": "Utilisateur supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
