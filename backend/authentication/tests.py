from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class BaseAuthTestCase(APITestCase):
    def setUp(self):
        # Création d'un utilisateur normal et d'un admin
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpass"
        )
        # Définition des URLs d'authentification
        self.LOGIN_URL = "/authentication/token/"
        self.TOKEN_REFRESH_URL = "/authentication/token/refresh/"
        self.LOGOUT_URL = "/authentication/logout/"
        self.RESET_PASSWORD_URL = "/authentication/reset-password/"

    def get_access_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def get_refresh_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh)

# --- LOGIN tests ---
class LoginTests(BaseAuthTestCase):
    def test_login_success_with_testuser(self):
        response = self.client.post(
            self.LOGIN_URL,
            {"username": "testuser", "password": "password123"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_login_success_with_admin(self):
        response = self.client.post(
            self.LOGIN_URL,
            {"username": "admin", "password": "adminpass"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_login_fail_wrong_password(self):
        response = self.client.post(
            self.LOGIN_URL,
            {"username": "testuser", "password": "wrongpassword"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# --- TOKEN REFRESH tests ---
class TokenRefreshTests(BaseAuthTestCase):
    def test_refresh_token_success_for_testuser(self):
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(
            self.TOKEN_REFRESH_URL,
            {"refresh": str(refresh)},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_refresh_token_success_for_admin(self):
        refresh = RefreshToken.for_user(self.admin)
        response = self.client.post(
            self.TOKEN_REFRESH_URL,
            {"refresh": str(refresh)},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_refresh_token_fail_invalid_token(self):
        response = self.client.post(
            self.TOKEN_REFRESH_URL,
            {"refresh": "invalidtoken"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# --- LOGOUT tests ---
class LogoutTests(BaseAuthTestCase):
    def test_logout_success_for_testuser(self):
        self.client.force_authenticate(user=self.user)
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(
            self.LOGOUT_URL,
            {"refresh": str(refresh)},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_logout_success_for_admin(self):
        self.client.force_authenticate(user=self.admin)
        refresh = RefreshToken.for_user(self.admin)
        response = self.client.post(
            self.LOGOUT_URL,
            {"refresh": str(refresh)},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_logout_fail_invalid_token(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.LOGOUT_URL,
            {"refresh": "invalidtoken"},
            format="json"
        )
        # Dans notre vue, un token invalide retourne un 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# --- RESET PASSWORD tests ---
class ResetPasswordTests(BaseAuthTestCase):
    def test_reset_password_success_for_testuser(self):
        response = self.client.post(
            self.RESET_PASSWORD_URL,
            {"email": "test@example.com"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_success_for_admin(self):
        response = self.client.post(
            self.RESET_PASSWORD_URL,
            {"email": "admin@example.com"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_fail_nonexistent_email(self):
        response = self.client.post(
            self.RESET_PASSWORD_URL,
            {"email": "nonexistent@example.com"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
