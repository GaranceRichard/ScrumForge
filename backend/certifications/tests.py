from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from certifications.models import Certification, Competency, CertificationCompetency
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image

User = get_user_model()

def get_test_image_file():
    # Crée une image 10x10 pixels en RGB et retourne ses bytes
    image = Image.new("RGB", (10, 10), color="red")
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    return buffer.getvalue()


class CertificationAPITests(APITestCase):
    def setUp(self):
        # Création d'un admin et d'un utilisateur non-admin
        self.admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass')
        self.user = User.objects.create_user(username='user', email='user@example.com', password='userpass')
        self.cert_list_url = '/certifications/'
        # Pour les tests d'association, créer une compétence
        self.competency = Competency.objects.create(name="Test Competency", description="Une compétence de test")

    # ----------------- Tests classiques ---------------------
    def test_create_certification_admin_valid(self):
        self.client.force_authenticate(user=self.admin)
        data = {"name": "Certification Test", "description": "Une certification de test"}
        response = self.client.post(self.cert_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Certification Test")

    def test_create_certification_admin_with_logo_valid(self):
        self.client.force_authenticate(user=self.admin)
        dummy_image = SimpleUploadedFile("logo.jpg", get_test_image_file(), content_type="image/jpeg")
        data = {
            "name": "Certification Logo",
            "description": "Certification avec logo",
            "logo": dummy_image
        }
        response = self.client.post(self.cert_list_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("logo", response.data)

    def test_create_certification_non_admin_fail(self):
        self.client.force_authenticate(user=self.user)
        data = {"name": "Cert NonAdmin", "description": "Devrait échouer"}
        response = self.client.post(self.cert_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_certifications_valid(self):
        Certification.objects.create(name="Cert List", description="Test liste")
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.cert_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_certifications_valid_with_existing(self):
        Certification.objects.create(name="Cert Existante", description="Déjà présente")
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.cert_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Cert Existante", [cert['name'] for cert in response.data])

    def test_list_certifications_invalid_method_fail(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.cert_list_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_certification_detail_valid(self):
        cert = Certification.objects.create(name="Cert Detail", description="Détail test")
        self.client.force_authenticate(user=self.admin)
        url = f"/certifications/{cert.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Cert Detail")

    def test_certification_detail_valid_includes_competencies(self):
        cert = Certification.objects.create(name="Cert Avec Comp", description="Test comp")
        # Créer une association
        CertificationCompetency.objects.create(certification=cert, competency=self.competency)
        self.client.force_authenticate(user=self.admin)
        url = f"/certifications/{cert.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Vérifier que la liste des compétences n'est pas vide
        self.assertGreater(len(response.data.get('competencies', [])), 0)

    def test_certification_detail_nonexistent_fail(self):
        self.client.force_authenticate(user=self.admin)
        url = "/certifications/9999/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_certification_admin_valid(self):
        cert = Certification.objects.create(name="Cert Update", description="Ancienne description")
        url = f"/certifications/{cert.id}/"
        self.client.force_authenticate(user=self.admin)
        data = {"name": "Cert Update Modifiée", "description": "Nouvelle description"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Cert Update Modifiée")

    def test_update_certification_admin_valid_logo(self):
        cert = Certification.objects.create(name="Cert Update Logo", description="Desc initiale")
        url = f"/certifications/{cert.id}/"
        self.client.force_authenticate(user=self.admin)
        dummy_image = SimpleUploadedFile("new_logo.jpg", get_test_image_file(), content_type="image/jpeg")
        data = {"logo": dummy_image}
        response = self.client.patch(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("logo", response.data)

    def test_update_certification_non_admin_fail(self):
        cert = Certification.objects.create(name="Cert NonUpdate", description="Ne doit pas se modifier")
        url = f"/certifications/{cert.id}/"
        self.client.force_authenticate(user=self.user)
        data = {"name": "Tentative de modification"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_certification_admin_valid(self):
        cert = Certification.objects.create(name="Cert Delete", description="À supprimer")
        url = f"/certifications/{cert.id}/"
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_certification_admin_valid_2(self):
        cert = Certification.objects.create(name="Cert Delete 2", description="Test suppression")
        url = f"/certifications/{cert.id}/"
        self.client.force_authenticate(user=self.admin)
        self.client.delete(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_certification_non_admin_fail(self):
        cert = Certification.objects.create(name="Cert NonDelete", description="Suppression interdite")
        url = f"/certifications/{cert.id}/"
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_certification_competencies_admin_valid(self):
        cert = Certification.objects.create(name="Cert Assoc", description="Assoc test")
        url = f"/certifications/{cert.id}/competencies/"
        self.client.force_authenticate(user=self.admin)
        data = {"competency_ids": [self.competency.id]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(CertificationCompetency.objects.filter(certification=cert, competency=self.competency).exists())

    def test_update_certification_competencies_admin_valid_empty(self):
        cert = Certification.objects.create(name="Cert Assoc Vide", description="Test sans associations")
        CertificationCompetency.objects.create(certification=cert, competency=self.competency)
        url = f"/certifications/{cert.id}/competencies/"
        self.client.force_authenticate(user=self.admin)
        data = {"competency_ids": []}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(cert.certificationcompetency_set.exists())

    def test_update_certification_competencies_non_admin_fail(self):
        cert = Certification.objects.create(name="Cert Assoc NonAdmin", description="Test non admin")
        url = f"/certifications/{cert.id}/competencies/"
        self.client.force_authenticate(user=self.user)
        data = {"competency_ids": [self.competency.id]}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ------------ Tests complémentaires pour utilisateurs non authentifiés ------------
    def test_list_certifications_non_authenticated_fail(self):
        # Pas de force_authenticate() => utilisateur non authentifié
        response = self.client.get(self.cert_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_certification_detail_non_authenticated_fail(self):
        cert = Certification.objects.create(name="Cert Detail NonAuth", description="Test non auth")
        url = f"/certifications/{cert.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CompetencyAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin2', email='admin2@example.com', password='adminpass')
        self.user = User.objects.create_user(username='user2', email='user2@example.com', password='userpass')
        self.comp_list_url = '/certifications/competencies/'

    # Création d'une compétence (Admin)
    def test_create_competency_admin_valid(self):
        self.client.force_authenticate(user=self.admin)
        data = {"name": "Compétence Test", "description": "Description de test"}
        response = self.client.post(self.comp_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Compétence Test")

    def test_create_competency_admin_valid_extra(self):
        self.client.force_authenticate(user=self.admin)
        data = {"name": "Compétence Extra", "description": "Une autre description"}
        response = self.client.post(self.comp_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_competency_non_admin_fail(self):
        self.client.force_authenticate(user=self.user)
        data = {"name": "Compétence NonAdmin", "description": "Devrait échouer"}
        response = self.client.post(self.comp_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Liste des compétences
    def test_list_competencies_valid(self):
        Competency.objects.create(name="Comp List", description="Test liste")
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.comp_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_competencies_valid_with_existing(self):
        Competency.objects.create(name="Comp Existante", description="Déjà présente")
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.comp_list_url)
        names = [comp['name'] for comp in response.data]
        self.assertIn("Comp Existante", names)

    def test_list_competencies_invalid_method_fail(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.comp_list_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # Détail d'une compétence
    def test_competency_detail_valid(self):
        comp = Competency.objects.create(name="Comp Detail", description="Test détail")
        url = f"/certifications/competencies/{comp.id}/"
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Comp Detail")

    def test_competency_detail_valid_again(self):
        comp = Competency.objects.create(name="Comp Detail 2", description="Autre détail")
        url = f"/certifications/competencies/{comp.id}/"
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_competency_detail_nonexistent_fail(self):
        self.client.force_authenticate(user=self.admin)
        url = "/certifications/competencies/9999/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Mise à jour d'une compétence (Admin)
    def test_update_competency_admin_valid(self):
        comp = Competency.objects.create(name="Comp Update", description="Ancienne desc")
        url = f"/certifications/competencies/{comp.id}/"
        self.client.force_authenticate(user=self.admin)
        data = {"name": "Comp Update Modifiée", "description": "Nouvelle desc"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Comp Update Modifiée")

    def test_update_competency_admin_valid_description(self):
        comp = Competency.objects.create(name="Comp Update 2", description="Desc initiale")
        url = f"/certifications/competencies/{comp.id}/"
        self.client.force_authenticate(user=self.admin)
        data = {"description": "Desc mise à jour"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], "Desc mise à jour")

    def test_update_competency_non_admin_fail(self):
        comp = Competency.objects.create(name="Comp NoUpdate", description="Desc initiale")
        url = f"/certifications/competencies/{comp.id}/"
        self.client.force_authenticate(user=self.user)
        data = {"name": "Modification interdite"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Suppression d'une compétence (Admin)
    def test_delete_competency_admin_valid(self):
        comp = Competency.objects.create(name="Comp Delete", description="À supprimer")
        url = f"/certifications/competencies/{comp.id}/"
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_competency_admin_valid_2(self):
        comp = Competency.objects.create(name="Comp Delete 2", description="Test suppression")
        url = f"/certifications/competencies/{comp.id}/"
        self.client.force_authenticate(user=self.admin)
        self.client.delete(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_competency_non_admin_fail(self):
        comp = Competency.objects.create(name="Comp NonDelete", description="Suppression interdite")
        url = f"/certifications/competencies/{comp.id}/"
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ------------ Tests complémentaires pour utilisateurs non authentifiés ------------
    def test_list_competencies_non_authenticated_fail(self):
        response = self.client.get(self.comp_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_competency_detail_non_authenticated_fail(self):
        comp = Competency.objects.create(name="Comp Detail NonAuth", description="Test non auth")
        url = f"/certifications/competencies/{comp.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
