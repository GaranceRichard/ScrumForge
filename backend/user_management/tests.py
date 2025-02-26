from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

# ----------------------------
# Tests pour l'opération "Register"
# ----------------------------
class UserRegisterTests(APITestCase):
    def test_register_user_success_valid(self):
        url = reverse('user-register')
        data = {"username": "newuser", "email": "newuser@example.com", "password": "StrongPass123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)

    def test_register_user_success_as_non_authenticated(self):
        url = reverse('user-register')
        data = {"username": "anotheruser", "email": "anotheruser@example.com", "password": "AnotherPass123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "anotheruser")

    def test_register_user_failure_missing_field(self):
        url = reverse('user-register')
        # Suppression du champ "email"
        data = {"username": "failuser", "password": "FailPass123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# ----------------------------
# Tests pour l'opération "Liste des utilisateurs" (admin seulement)
# ----------------------------
class UserListTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin", email="admin@example.com", password="adminpass")
        self.user1 = User.objects.create_user(username="user1", email="user1@example.com", password="pass123")
        self.user2 = User.objects.create_user(username="user2", email="user2@example.com", password="pass123")
        self.url = reverse('user-list')

    def test_list_users_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usernames = [user['username'] for user in response.data]
        self.assertIn("user1", usernames)
        self.assertIn("user2", usernames)

    def test_list_users_ordered_by_username(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usernames = [user['username'] for user in response.data]
        self.assertEqual(usernames, sorted(usernames))

    def test_list_users_failure_non_admin(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# ----------------------------
# Tests pour l'opération "Détail d'un utilisateur" (admin seulement)
# ----------------------------
class UserDetailTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin", email="admin@example.com", password="adminpass")
        self.user = User.objects.create_user(username="userdetail", email="userdetail@example.com", password="pass123")
        self.url = reverse('user-detail', kwargs={'pk': self.user.id})

    def test_user_detail_success_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "userdetail")
        self.assertEqual(response.data["email"], "userdetail@example.com")

    def test_user_detail_contains_required_fields(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)
        self.assertIn("last_login", response.data)

    def test_user_detail_failure_non_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# ----------------------------
# Tests pour l'opération "Mise à jour de son propre profil"
# ----------------------------
class UserSelfUpdateTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="selfuser", email="selfuser@example.com", password="pass123")
        self.url = reverse('user-self-update')

    def test_self_update_success_change_username(self):
        self.client.force_authenticate(user=self.user)
        data = {"username": "updatedselfuser"}
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "updatedselfuser")

    def test_self_update_success_change_email_and_password(self):
        self.client.force_authenticate(user=self.user)
        data = {"email": "updated@example.com", "password": "NewStrongPass123"}
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "updated@example.com")
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewStrongPass123"))

    def test_self_update_failure_unauthenticated(self):
        data = {"username": "shouldfail"}
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# ----------------------------
# Tests pour l'opération "Mise à jour d'un utilisateur par un admin"
# ----------------------------
class UserAdminUpdateTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin", email="admin@example.com", password="adminpass")
        self.user = User.objects.create_user(username="normaluser", email="normal@example.com", password="pass123")
        self.url = reverse('user-admin-update', kwargs={'pk': self.user.id})

    def test_admin_update_success_change_username(self):
        self.client.force_authenticate(user=self.admin)
        data = {"username": "updateduser"}
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "updateduser")

    def test_admin_update_success_change_password(self):
        self.client.force_authenticate(user=self.admin)
        data = {"password": "NewPass123"}
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewPass123"))

    def test_admin_update_failure_non_admin(self):
        self.client.force_authenticate(user=self.user)
        data = {"username": "hackedusername"}
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# ----------------------------
# Tests pour l'opération "Suppression d'un utilisateur par un admin"
# ----------------------------
class UserDeleteTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin", email="admin@example.com", password="adminpass")
        self.user = User.objects.create_user(username="tobedeleted", email="tobedeleted@example.com", password="pass123")
        self.url = reverse('user-delete', kwargs={'pk': self.user.id})

    def test_delete_user_success_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.user.id)

    def test_delete_user_success_after_deletion_returns_404(self):
        self.client.force_authenticate(user=self.admin)
        self.client.delete(self.url)
        detail_url = reverse('user-detail', kwargs={'pk': self.user.id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_user_failure_non_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
