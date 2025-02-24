from unittest.mock import patch
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class BaseTestCase(APITestCase):
    """Classe de base pour éviter la répétition du setup"""

    def setUp(self):
        """Créer les utilisateurs communs à tous les tests"""
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpass"
        )
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", email="other@example.com", password="password456"
        )

        # Assurer que SEUL l'admin est `is_staff=True`
        self.admin.is_staff = True
        self.admin.save()
        self.user.is_staff = False
        self.user.save()
        self.other_user.is_staff = False
        self.other_user.save()

        # URLs pour les tests
        self.LOGIN_URL = "/authentication/token/"
        self.TOKEN_REFRESH_URL = "/authentication/token/refresh/"
        self.LOGOUT_URL = "/authentication/logout/"
        self.USER_LIST_URL = "/authentication/users/"
        self.USER_UPDATE_URL = "/authentication/users/{}/update/"
        self.USER_SELF_UPDATE_URL = "/authentication/users/self-update/"
        self.USER_DELETE_URL = "/authentication/users/{}/delete/"
        self.USER_REGISTER_URL = "/authentication/register/"
        self.RESET_PASSWORD_URL = "/authentication/reset-password/"

    def get_access_token(self, user):
        """Récupérer un token JWT pour un utilisateur donné"""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def get_refresh_token(self, user):
        """Récupérer un refresh token pour un utilisateur donné"""
        refresh = RefreshToken.for_user(user)
        return str(refresh)

    def authenticate_user(self, user):
        """Authentifier un utilisateur avec son token"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.get_access_token(user)}")


# -----------------------------
# Tests pour l'authentification
# -----------------------------
class AuthenticationTests(BaseTestCase):

    def test_obtain_jwt_token_success(self):
        """✅ Vérifie qu'on peut obtenir un token JWT"""
        response = self.client.post(self.LOGIN_URL, {"username": "testuser", "password": "password123"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_obtain_jwt_token_fail(self):
        """❌ Échec avec un mauvais mot de passe"""
        response = self.client.post(self.LOGIN_URL, {"username": "testuser", "password": "wrongpassword"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_success(self):
        """✅ Vérifie qu'on peut rafraîchir un token JWT"""
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(self.TOKEN_REFRESH_URL, {"refresh": str(refresh)}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_refresh_token_fail(self):
        """❌ Test de rafraîchissement avec un refresh token invalide"""
        response = self.client.post(self.TOKEN_REFRESH_URL, {"refresh": "invalid_token"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_success(self):
        """✅ Vérifie qu'un utilisateur peut se déconnecter"""
        self.authenticate_user(self.user)
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(self.LOGOUT_URL, {"refresh": str(refresh)}, format="json")
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_logout_fail(self):
        """❌ Test de déconnexion avec un refresh token invalide"""
        response = self.client.post(self.LOGOUT_URL, {"refresh": "invalid_token"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# -----------------------------
# Tests pour l'inscription
# -----------------------------
class RegisterTests(BaseTestCase):

    def test_register_success(self):
        """✅ Inscription réussie"""
        data = {"username": "newuser", "email": "newuser@example.com", "password": "SecurePass123!"}
        response = self.client.post(self.USER_REGISTER_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_fail_missing_email(self):
        """❌ Échec si l'email est manquant"""
        data = {"username": "userwithoutemail", "password": "SecurePass123!"}
        response = self.client.post(self.USER_REGISTER_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# -----------------------------
# Tests pour la liste des utilisateurs
# -----------------------------
class UserListTests(BaseTestCase):

    def test_list_users_as_admin(self):
        """✅ Un admin peut voir la liste des utilisateurs"""
        self.authenticate_user(self.admin)
        response = self.client.get(self.USER_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_users_as_normal_user(self):
        """❌ Un utilisateur normal ne peut pas voir la liste des utilisateurs"""
        self.authenticate_user(self.user)
        response = self.client.get(self.USER_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# -----------------------------
# Tests pour la mise à jour des utilisateurs
# -----------------------------
class UserUpdateTests(BaseTestCase):

    def test_admin_can_update_user(self):
        """✅ Un admin peut modifier un utilisateur"""
        self.authenticate_user(self.admin)
        response = self.client.patch(self.USER_UPDATE_URL.format(self.user.id), {"username": "updated_user"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "updated_user")

    def test_user_cannot_update_other_user(self):
        """❌ Un utilisateur ne peut pas modifier le profil d'un autre utilisateur"""
        self.authenticate_user(self.user)
        response = self.client.patch(self.USER_UPDATE_URL.format(self.other_user.id), {"username": "hacked_username"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# -----------------------------
# Tests pour la mise à jour du propre profil utilisateur
# -----------------------------
class UserSelfUpdateTests(BaseTestCase):

    def test_user_can_update_own_info(self):
        """✅ Un utilisateur peut modifier son propre profil"""
        self.authenticate_user(self.user)
        response = self.client.patch(self.USER_SELF_UPDATE_URL, {"username": "newusername"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_cannot_update_profile(self):
        """❌ Un utilisateur non authentifié ne peut pas modifier son profil"""
        response = self.client.patch(self.USER_SELF_UPDATE_URL, {"username": "newusername"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# -----------------------------
# Tests pour la suppression des utilisateurs
# -----------------------------
class UserDeleteTests(BaseTestCase):

    def test_admin_can_delete_user(self):
        """✅ Un admin peut supprimer un utilisateur"""
        self.authenticate_user(self.admin)
        response = self.client.delete(self.USER_DELETE_URL.format(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_cannot_delete_superuser(self):
        """❌ Un admin ne peut pas supprimer un superutilisateur"""
        self.authenticate_user(self.admin)
        superuser = User.objects.create_superuser(username="superadmin", email="superadmin@example.com", password="adminpass")
        response = self.client.delete(self.USER_DELETE_URL.format(superuser.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# -----------------------------
# Tests pour la réinitialisation du mot de passe
# -----------------------------
class ResetPasswordTests(BaseTestCase):

    def test_reset_password_success(self):
        """✅ Vérifie qu'un utilisateur peut réinitialiser son mot de passe"""
        response = self.client.post(self.RESET_PASSWORD_URL, {"email": "test@example.com"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_fail_email_not_found(self):
        """❌ Vérifie que l'API retourne une erreur 404 si l'email n'existe pas"""
        response = self.client.post(self.RESET_PASSWORD_URL, {"email": "unknown@example.com"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# -----------------------------
# Tests pour l'authentification sociale (mockée)
# -----------------------------
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class SocialAuthMockTests(APITestCase):
    """Test des fonctionnalités d'authentification sociale avec mock"""

    def setUp(self):
        """Créer un utilisateur simulé pour le test"""
        self.user_google = User.objects.create_user(
            username="google_user", email="google_user@example.com", password="password"
        )
        self.user_linkedin = User.objects.create_user(
            username="linkedin_user", email="linkedin_user@example.com", password="password"
        )

    def get_access_token(self, user):
        """Récupérer un token JWT pour un utilisateur donné"""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    @patch('social_core.backends.google.GoogleOAuth2.authenticate')
    def test_google_login_successful(self, MockGoogleAuth):
        """✅ Test de la connexion via Google avec mock"""
        # Simuler la réponse d'un utilisateur Google
        MockGoogleAuth.return_value = MagicMock(
            get_user=lambda request: self.user_google
        )

        # Simuler une requête de connexion via Google avec un token valide
        response = self.client.post('/authentication/token/', {
            'username': 'google_user',
            'email': 'google_user@example.com',
            'password': 'password'
        }, HTTP_AUTHORIZATION=f'Bearer {self.get_access_token(self.user_google)}', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # Vérifie que le token est retourné

    @patch('social_core.backends.linkedin.LinkedinOAuth2.authenticate')
    def test_linkedin_login_successful(self, MockLinkedinAuth):
        """✅ Test de la connexion via LinkedIn avec mock"""
        # Simuler la réponse d'un utilisateur LinkedIn
        MockLinkedinAuth.return_value = MagicMock(
            get_user=lambda request: self.user_linkedin
        )

        # Simuler une requête de connexion via LinkedIn avec un token valide
        response = self.client.post('/authentication/token/', {
            'username': 'linkedin_user',
            'email': 'linkedin_user@example.com',
            'password': 'password'
        }, HTTP_AUTHORIZATION=f'Bearer {self.get_access_token(self.user_linkedin)}', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # Vérifie que le token est retourné

    def test_google_login_fail(self):
        """❌ Test échouant avec un mauvais mot de passe pour Google"""
        response = self.client.post('/authentication/token/', {
            'username': 'google_user',
            'email': 'google_user@example.com',
            'password': 'wrongpassword'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_linkedin_login_fail(self):
        """❌ Test échouant avec un mauvais mot de passe pour LinkedIn"""
        response = self.client.post('/authentication/token/', {
            'username': 'linkedin_user',
            'email': 'linkedin_user@example.com',
            'password': 'wrongpassword'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
