from django.urls import path
from .views import (
    UserRegisterView,
    UserListView,
    UserDetailView,
    UserSelfUpdateView,
    UserAdminUpdateView,
    UserDeleteView,
)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/self/', UserSelfUpdateView.as_view(), name='user-self-update'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/update/', UserAdminUpdateView.as_view(), name='user-admin-update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
]
