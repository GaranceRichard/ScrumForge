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

    def test_refresh_token(self):
        """Vérifie qu'un utilisateur peut rafraîchir son token d'accès"""
        refresh = RefreshToken.for_user(self.user)
        refresh_token = str(refresh)

        response = self.client.post("/authentication/token/refresh/", {"refresh": refresh_token}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)  # Vérifie qu'on reçoit bien un nouveau access token

    def test_refresh_token_invalid(self):
        """Vérifie qu'un refresh token invalide ne permet PAS d'obtenir un nouvel access token"""
        invalid_refresh_token = "invalid_token_string"

        response = self.client.post("/authentication/token/refresh/", {"refresh": invalid_refresh_token}, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Django doit refuser l'accès
        self.assertIn("detail", response.data)  # Vérifie que le message d'erreur est présent
        self.assertEqual(response.data["detail"], "Token is invalid or expired")  # Vérifie le message d'erreur exact

    def test_access_home_authenticated(self):
        """Vérifie qu'un utilisateur authentifié peut accéder à la page d'accueil"""
        # Obtenir un token JWT
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        # Ajouter le token dans le header Authorization
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # OK si authentifié
        self.assertIn("message", response.data)  # Vérifie la présence d'un message
        self.assertEqual(response.data["message"], "Bienvenue sur l'API !")  # Vérifie le bon message

    def test_access_home_unauthenticated(self):
        """Vérifie qu'un utilisateur non authentifié ne peut PAS accéder à la page d'accueil"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Accès refusé sans token
        self.assertIn("detail", response.data)  # Vérifie que Django renvoie un message d'erreur
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")  # Vérifie le message d'erreur exact

    def test_logout_success(self):
        """Vérifie qu'un utilisateur peut se déconnecter et que son refresh token est blacklisté"""
        refresh = RefreshToken.for_user(self.user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)

        # Ajouter le token d'authentification dans les headers
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # Envoyer la requête de logout
        response = self.client.post("/authentication/logout/", {"refresh": refresh_token}, format="json")

        # Vérifier que la requête a bien été traitée
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(response.data["message"], "Déconnexion réussie.")

        # Vérifier que le refresh token est maintenant invalide
        response = self.client.post("/authentication/token/refresh/", {"refresh": refresh_token}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Token is blacklisted")


    def test_logout_invalid_token(self):
        """Vérifie qu'un utilisateur ne peut PAS se déconnecter avec un refresh token invalide"""
        invalid_refresh_token = "invalid_token_string"

        # Ajouter le token d'authentification dans les headers
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # Envoyer une requête de logout avec un refresh token invalide
        response = self.client.post("/authentication/logout/", {"refresh": invalid_refresh_token}, format="json")

        # Vérifier que la requête est refusée avec une erreur 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Token invalide ou déjà expiré.")
