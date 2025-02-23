from django.http import JsonResponse
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    LogoutView, RegisterView, ResetPasswordView, UserListView,
    UserUpdateView, UserSelfUpdateView, UserDeleteView
)

urlpatterns = [
    # 🔐 Authentification
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login API
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh Token
    path('logout/', LogoutView.as_view(), name='logout'),  # Logout API
    path('register/', RegisterView.as_view(), name='register'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),

    # 👥 Gestion des utilisateurs
    path('users/', UserListView.as_view(), name='user-list'),  # 🔹 Liste des utilisateurs (Admin)
    path('users/update/', UserSelfUpdateView.as_view(), name='user-self-update'),  # 🔹 Mise à jour par l'utilisateur connecté
    path('users/<int:user_id>/', UserUpdateView.as_view(), name='user-update'),  # 🔹 Mise à jour par un admin
    path('users/<int:user_id>/delete/', UserDeleteView.as_view(), name='user-delete'),  # 🔹 Suppression par un admin
]

# 🚀 Gestion des erreurs 404
def custom_404(request, exception):
    return JsonResponse({"error": "Ressource non trouvée."}, status=404)

handler404 = "backend.urls.custom_404"
