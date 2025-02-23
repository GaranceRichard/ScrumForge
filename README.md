# ScrumForge

# 📌 Authentication API

## 🚀 Présentation
L'API **Authentication** est un service développé avec **Django Rest Framework (DRF)** qui gère l'authentification et la gestion des utilisateurs. Elle permet l'inscription, la connexion, la mise à jour et la suppression des utilisateurs avec un système sécurisé basé sur des tokens d'authentification.

## 🏗 Architecture de l'API
L'API repose sur les composants suivants :

- **Django Rest Framework (DRF)** : gestion des endpoints et des permissions.
- **JWT (JSON Web Token)** : authentification sécurisée des utilisateurs.
- **PostgreSQL / SQLite** : base de données utilisateur.
- **Django User Model** : gestion des utilisateurs.
- **Serializers** : conversion des objets en JSON.

## 📁 Structure du projet
```
/authentication
│── /migrations               # Migrations de la base de données
│── /models.py                # Modèles utilisateur
│── /serializers.py           # Sérialisation des données
│── /views.py                 # Logique métier des endpoints
│── /urls.py                  # Routage des API endpoints
│── /permissions.py           # Gestion des permissions
│── /tests.py                 # Tests unitaires
│── tokens.py                 # Gestion des tokens JWT
│── settings.py               # Configuration du projet
│── wsgi.py / asgi.py         # Serveur d’application
```

## 🛠 Endpoints de l'API
Tous les endpoints sont accessibles via `/api/auth/`

### 🔹 1. Inscription
- **Méthode** : `POST`
- **URL** : `/api/auth/register/`
- **Corps de la requête** :
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```
- **Réponse** :
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "message": "Compte créé avec succès"
}
```

### 🔹 2. Connexion
- **Méthode** : `POST`
- **URL** : `/api/auth/login/`
- **Corps de la requête** :
```json
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```
- **Réponse** :
```json
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}
```

### 🔹 3. Rafraîchir le Token JWT
- **Méthode** : `POST`
- **URL** : `/api/auth/refresh/`

### 🔹 4. Déconnexion
- **Méthode** : `POST`
- **URL** : `/api/auth/logout/`

### 🔹 5. Profil utilisateur
- **Méthode** : `GET`
- **URL** : `/api/auth/me/`

### 🔹 6. Mise à jour du profil
- **Méthode** : `PUT`
- **URL** : `/api/auth/update/`

### 🔹 7. Suppression du compte
- **Méthode** : `DELETE`
- **URL** : `/api/auth/delete/`

## 🔐 Sécurité
- Utilisation de **JWT** pour l'authentification.
- L’**access token** est utilisé pour accéder aux endpoints sécurisés.
- Le **refresh token** permet de renouveler l’access token.

## 📦 Installation et exécution
1. **Cloner le projet**
```bash
git clone https://github.com/votre-repo/auth-api.git
cd auth-api
```

2. **Créer un environnement virtuel et installer les dépendances**
```bash
python3 -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
pip install -r requirements.txt
```

3. **Appliquer les migrations**
```bash
python manage.py migrate
```

4. **Créer un super-utilisateur**
```bash
python manage.py createsuperuser
```

5. **Lancer le serveur**
```bash
python manage.py runserver
```

L'API sera accessible à `http://127.0.0.1:8000/api/auth/`.

## 🛠 Technologies utilisées
- Python 3.x
- Django & Django Rest Framework
- PostgreSQL / SQLite
- JWT pour l'authentification

## 📌 À venir
✅ Implémentation des rôles et permissions avancées  
✅ Gestion des mots de passe oubliés  
✅ Support OAuth (Google, GitHub, etc.)  

---
💡 **Auteur** : Garance Richard
📧 Contact : garance.richard@gmail.com
📅 Dernière mise à jour : Février 2025  
