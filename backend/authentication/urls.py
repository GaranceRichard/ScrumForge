from django.http import JsonResponse
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import LogoutView, ResetPasswordView

urlpatterns = [
    # 🔐 Authentification
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login API
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh Token
    path('logout/', LogoutView.as_view(), name='logout'),  # Logout API
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('auth/', include('social_django.urls', namespace='social')),  # Routes d'authentification 

]

# 🚀 Gestion des erreurs 404
def custom_404(request, exception):
    return JsonResponse({"error": "Ressource non trouvée."}, status=404)

handler404 = "backend.urls.custom_404"
