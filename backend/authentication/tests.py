from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class BaseTestCase(APITestCase):
    """Classe de base pour éviter la répétition du setup"""

    def setUp(self):
        """Créer les utilisateurs communs à tous les tests"""
        self.admin = User.objects.create_superuser(username="admin", email="admin@example.com", password="adminpass")
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        self.other_user = User.objects.create_user(username="otheruser", email="other@example.com", password="password456")

        # URLs
        self.LOGIN_URL = "/authentication/token/"
        self.USER_LIST_URL = "/authentication/users/"
        self.USER_UPDATE_URL = "/authentication/users/update/"
        self.USER_DELETE_URL = "/authentication/users/{id}/delete/"
        self.USER_REGISTER_URL = "/authentication/register/"
        self.RESET_PASSWORD_URL = "/authentication/reset-password/"

    def get_access_token(self, user):
        """Récupérer un token JWT pour un utilisateur donné"""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def authenticate_user(self, user):
        """Authentifier un utilisateur avec son token"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.get_access_token(user)}")


class AuthenticationTests(BaseTestCase):
    """Tests pour l'authentification"""

    def test_obtain_jwt_token(self):
        """✅ Vérifie qu'on peut obtenir un token JWT"""
        response = self.client.post(self.LOGIN_URL, {"username": "testuser", "password": "password123"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_refresh_token(self):
        """✅ Vérifie qu'un utilisateur peut rafraîchir son token"""
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post("/authentication/token/refresh/", {"refresh": str(refresh)}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_access_home_authenticated(self):
        """✅ Vérifie qu'un utilisateur authentifié peut accéder à la page d'accueil"""
        self.authenticate_user(self.user)
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

    def test_access_home_unauthenticated(self):
        """❌ Vérifie qu'un utilisateur non authentifié ne peut PAS accéder à la page d'accueil"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RegisterTests(BaseTestCase):
    """Tests pour l'inscription"""

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


class UserListTests(BaseTestCase):
    """Tests pour la liste des utilisateurs"""

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


class UserUpdateTests(BaseTestCase):
    """Tests pour la mise à jour des utilisateurs"""

    def test_admin_can_update_user(self):
        """✅ Un admin peut modifier un utilisateur"""
        self.authenticate_user(self.admin)
        response = self.client.patch(self.USER_UPDATE_URL, {"user_id": self.user.id, "username": "updated_user"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "updated_user")

    def test_user_can_update_own_info(self):
        """✅ Un utilisateur peut modifier son propre profil"""
        self.authenticate_user(self.user)
        response = self.client.patch(self.USER_UPDATE_URL, {"username": "newusername"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserDeleteTests(BaseTestCase):
    """Tests pour la suppression d'un utilisateur"""

    def test_admin_can_delete_user(self):
        """✅ Un admin peut supprimer un utilisateur"""
        self.authenticate_user(self.admin)
        response = self.client.delete(self.USER_DELETE_URL.format(id=self.user.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_cannot_delete_superuser(self):
        """❌ Un admin ne peut pas supprimer un superutilisateur"""
        self.authenticate_user(self.admin)
        superuser = User.objects.create_superuser(username="superadmin", email="superadmin@example.com", password="adminpass")
        response = self.client.delete(self.USER_DELETE_URL.format(id=superuser.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ResetPasswordTests(BaseTestCase):
    """Tests pour la réinitialisation de mot de passe"""

    def test_reset_password_success(self):
        """✅ Vérifie qu'un utilisateur peut réinitialiser son mot de passe"""
        response = self.client.post(self.RESET_PASSWORD_URL, {"email": "test@example.com"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_fail_email_not_found(self):
        """❌ Vérifie que l'API retourne une erreur 404 si l'email n'existe pas"""
        response = self.client.post(self.RESET_PASSWORD_URL, {"email": "unknown@example.com"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
