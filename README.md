ScrumForge
Le projet ScrumForge vise à proposer un espace où chaque inscrit peut travailler ses compétences sur les certifications Scrum.org et, grâce à un entraînement progressif, se préparer en toute confiance à passer ces certifications.

🏰 Backend
📌 Authentication API
L'API Authentication est un service développé avec Django Rest Framework (DRF) qui gère :

L'authentification JWT
La gestion des utilisateurs
L'authentification sociale (Google, LinkedIn)
L'administration sécurisée avec des permissions avancées
💁 Structure du projet
bash
Copier
/authentication
│── /migrations               # Migrations de la base de données
│── /models.py                # Modèles utilisateur
│── /serializers.py           # Sérialisation des données
│── /views.py                 # Logique métier des endpoints
│── /urls.py                  # Routage des API endpoints
│── /permissions.py           # Gestion des permissions
│── /tests.py                 # Tests unitaires
│── /tokens.py                # Gestion des tokens JWT
│── /social/                  # Gestion de l'authentification sociale (Google, LinkedIn)
│── settings.py               # Configuration du projet
│── wsgi.py / asgi.py         # Serveur d’application
🔹 Endpoints de l'Authentication API
Tous les endpoints d'authentification sont accessibles via /authentication/.

1. Inscription
Méthode : POST
URL : /authentication/register/
json
Copier
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}
Réponse :
json
Copier
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "message": "Compte créé avec succès"
}
2. Connexion (JWT)
Méthode : POST
URL : /authentication/token/
json
Copier
{
  "username": "john_doe",
  "password": "SecurePass123!"
}
Réponse :
json
Copier
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}
3. Rafraîchir le Token JWT
Méthode : POST
URL : /authentication/token/refresh/
4. Déconnexion
Méthode : POST
URL : /authentication/logout/
json
Copier
{
  "refresh": "jwt_refresh_token"
}
5. Profil utilisateur
Méthode : GET
URL : /authentication/users/me/
6. Mise à jour du profil (Utilisateur)
Méthode : PATCH
URL : /authentication/users/self-update/
7. Mise à jour d'un utilisateur (Admin)
Méthode : PATCH
URL : /authentication/users/<user_id>/update/
8. Suppression du compte (Admin)
Méthode : DELETE
URL : /authentication/users/<user_id>/delete/
9. Authentification sociale (Google, LinkedIn)
Connexion avec Google
Méthode : GET
URL : /auth/login/google/
Redirection : L'utilisateur est redirigé vers la page de connexion Google.
Connexion avec LinkedIn
Méthode : GET
URL : /auth/login/linkedin/
Redirection : L'utilisateur est redirigé vers la page de connexion LinkedIn.
Redirection après connexion sociale
Une fois authentifié via Google ou LinkedIn, l'utilisateur est redirigé vers l'application avec un token JWT.
🔹 Certification & Compétences API
En plus de l'API d'authentification, ScrumForge propose une API dédiée aux certifications Scrum.org et aux compétences qui leur sont associées. Pour cette API, toutes les opérations requièrent que l'utilisateur soit authentifié. Les opérations de création, de mise à jour et de suppression sont réservées aux administrateurs.

Endpoints pour Certifications
Les endpoints liés aux certifications sont accessibles via /certifications/.

Création d'une certification (Admin)

Méthode : POST
URL : /certifications/
Description : Permet à un administrateur de créer une certification.
(Les données peuvent inclure un logo, qui sera stocké dans backend/certification_logos/.)
Liste des certifications

Méthode : GET
URL : /certifications/
Description : Retourne la liste des certifications existantes.
Détail d'une certification (avec compétences rattachées)

Méthode : GET
URL : /certifications/<id>/
Description : Affiche les détails d'une certification, incluant la liste des compétences associées.
Mise à jour d'une certification (Admin)

Méthode : PATCH (ou PUT)
URL : /certifications/<id>/
Description : Permet à un administrateur de mettre à jour le nom, la description et le logo d'une certification.
Suppression d'une certification (Admin)

Méthode : DELETE
URL : /certifications/<id>/
Description : Permet à un administrateur de supprimer une certification.
Modification des associations Certification‑Compétences (Admin)

Méthode : PUT
URL : /certifications/<id>/competencies/
Description : Permet de mettre à jour la liste des compétences rattachées à une certification en fournissant une liste d'IDs de compétences.
Endpoints pour Compétences
Les endpoints liés aux compétences sont accessibles via /certifications/competencies/.

Création d'une compétence (Admin)

Méthode : POST
URL : /certifications/competencies/
Description : Permet à un administrateur de créer une compétence.
Liste des compétences

Méthode : GET
URL : /certifications/competencies/
Description : Retourne la liste des compétences disponibles.
Détail d'une compétence

Méthode : GET
URL : /certifications/competencies/<id>/
Description : Affiche le détail d'une compétence.
Mise à jour d'une compétence (Admin)

Méthode : PATCH (ou PUT)
URL : /certifications/competencies/<id>/
Description : Permet à un administrateur de mettre à jour le nom et la description d'une compétence.
Suppression d'une compétence (Admin)

Méthode : DELETE
URL : /certifications/competencies/<id>/
Description : Permet à un administrateur de supprimer une compétence.
🔒 Sécurité
JWT : utilisé pour l'authentification.
OAuth2 : pour l'authentification sociale (Google, LinkedIn).
Rôles et permissions avancées :
Utilisateur : doit être authentifié pour consulter les endpoints (GET).
Administrateur : requis pour les opérations de création, mise à jour et suppression.
🛠 Technologies utilisées
Python 3.x
Django & Django Rest Framework
PostgreSQL / SQLite
JWT pour l'authentification
Social Auth (Google, LinkedIn)
DRF Spectacular (Documentation API)
📈 Auteur : Garance Richard
📧 Contact : garance.richard@gmail.com
🗓 Dernière mise à jour : Février 2025

