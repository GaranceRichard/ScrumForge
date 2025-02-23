from django.http import JsonResponse
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import LogoutView, RegisterView, ResetPasswordView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login API
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh Token
    path('logout/', LogoutView.as_view(), name='logout'),  # Logout API
    path('register/', RegisterView.as_view(), name='register'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]

def custom_404(request, exception):
    return JsonResponse({"error": "Ressource non trouvée."}, status=404)

handler404 = "backend.urls.custom_404"