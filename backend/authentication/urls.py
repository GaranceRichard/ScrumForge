from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import LogoutView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login API
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh Token
     path('logout/', LogoutView.as_view(), name='logout'),  # Logout API
]
