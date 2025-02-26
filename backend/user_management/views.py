from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import (
    UserCreateSerializer,
    UserListSerializer,
    UserDetailSerializer,
    UserSelfUpdateSerializer,
    UserAdminUpdateSerializer,
)

User = get_user_model()

class UserRegisterView(generics.CreateAPIView):
    """
    Endpoint de création d'un nouvel utilisateur.
    Accessible par toute personne (non authentifiée ou admin).
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

class UserListView(generics.ListAPIView):
    """
    Endpoint pour lister tous les utilisateurs, triés par username.
    Accessible uniquement aux administrateurs.
    """
    queryset = User.objects.all().order_by('username')
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAdminUser]

class UserDetailView(generics.RetrieveAPIView):
    """
    Endpoint pour obtenir le détail d'un utilisateur (username, email, last_login).
    Accessible uniquement aux administrateurs.
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAdminUser]

class UserSelfUpdateView(generics.RetrieveUpdateAPIView):
    """
    Endpoint pour qu'un utilisateur mette à jour son propre profil.
    Accessible uniquement aux utilisateurs authentifiés.
    """
    serializer_class = UserSelfUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserAdminUpdateView(generics.RetrieveUpdateAPIView):
    """
    Endpoint permettant à un administrateur de mettre à jour un utilisateur.
    """
    queryset = User.objects.all()
    serializer_class = UserAdminUpdateSerializer
    permission_classes = [permissions.IsAdminUser]

from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import UserDeleteResponseSerializer

User = get_user_model()

class UserDeleteView(APIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserDeleteResponseSerializer

    def get_serializer_class(self):
        return self.serializer_class

    def delete(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        if user.is_superuser:
            return Response(
                {"error": "Impossible de supprimer un superutilisateur."},
                status=status.HTTP_403_FORBIDDEN
            )
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
