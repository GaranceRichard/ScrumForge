from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class AuthenticationTests(APITestCase):

    def setUp(self):
        # Création d'un utilisateur test
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.login_url = "/authentication/token/"
        self.dashboard_url = "/dashboard/"

    def test_obtain_jwt_token(self):
        """Vérifie qu'on peut obtenir un token JWT"""
        response = self.client.post(self.login_url, {"username": "testuser", "password": "password123"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_access_dashboard_without_authentication(self):
        """Vérifie qu'un utilisateur non authentifié ne peut PAS accéder au dashboard"""
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_dashboard_with_authentication(self):
        """Vérifie qu'un utilisateur authentifié PEUT accéder au dashboard"""
        # Obtenir un token JWT
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        # Ajouter le token dans le header Authorization
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Bienvenue sur le Dashboard")
