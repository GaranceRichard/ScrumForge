# ScrumForge
Le projet **ScrumForge** vise à proposer un espace où chaque inscrit peut travailler ses compétences sur les certifications Scrum.org et, grâce à un entraînement progressif, se préparer en toute confiance à passer ces certifications.

---

## 🏰 **Backend**
### 📌 **Authentication API**
L'API **Authentication** est un service développé avec **Django Rest Framework (DRF)** qui gère :
- L'**authentification JWT**
- La gestion des **utilisateurs**
- L'**authentification sociale** (Google, LinkedIn)
- L'administration sécurisée avec des **permissions avancées**

### 💁 **Structure du projet**
```
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
```

---

## 🛠 **Endpoints de l'API**
Tous les endpoints sont accessibles via `/authentication/`

### 🔹 **1. Inscription**
- **Méthode** : `POST`
- **URL** : `/authentication/register/`
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

### 🔹 **2. Connexion (JWT)**
- **Méthode** : `POST`
- **URL** : `/authentication/token/`
```json
{
  "username": "john_doe",
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

### 🔹 **3. Rafraîchir le Token JWT**
- **Méthode** : `POST`
- **URL** : `/authentication/token/refresh/`

### 🔹 **4. Déconnexion**
- **Méthode** : `POST`
- **URL** : `/authentication/logout/`
```json
{
  "refresh": "jwt_refresh_token"
}
```

### 🔹 **5. Profil utilisateur**
- **Méthode** : `GET`
- **URL** : `/authentication/users/me/`

### 🔹 **6. Mise à jour du profil (Utilisateur)**
- **Méthode** : `PATCH`
- **URL** : `/authentication/users/self-update/`

### 🔹 **7. Mise à jour d'un utilisateur (Admin)**
- **Méthode** : `PATCH`
- **URL** : `/authentication/users/<user_id>/update/`

### 🔹 **8. Suppression du compte (Admin)**
- **Méthode** : `DELETE`
- **URL** : `/authentication/users/<user_id>/delete/`

---

## 🔹 **9. Authentification sociale (Google, LinkedIn)**
L'API prend en charge l'authentification sociale via **Google** et **LinkedIn** en OAuth2.

### **Connexion avec Google**
- **Méthode** : `GET`
- **URL** : `/auth/login/google/`
- **Redirection** : L'utilisateur est redirigé vers la page de connexion Google.

### **Connexion avec LinkedIn**
- **Méthode** : `GET`
- **URL** : `/auth/login/linkedin/`
- **Redirection** : L'utilisateur est redirigé vers la page de connexion LinkedIn.

### **Redirection après connexion sociale**
Une fois authentifié via Google ou LinkedIn, l'utilisateur est redirigé vers l'application avec un **token JWT**.

---

## 🔒 **Sécurité**
- **JWT** : utilisé pour l'authentification.
- **OAuth2** : pour l'authentification sociale (Google, LinkedIn).
- **Rôles et permissions avancées** :
  - **Utilisateur** : accès à ses propres informations.
  - **Administrateur** : gestion des utilisateurs et des comptes.

---

## 🛠 **Technologies utilisées**
- Python 3.x
- Django & Django Rest Framework
- PostgreSQL / SQLite
- JWT pour l'authentification
- Social Auth (Google, LinkedIn)
- DRF Spectacular (Documentation API)

---

📈 **Auteur** : Garance Richard  
📧 **Contact** : garance.richard@gmail.com  
🗓 **Dernière mise à jour** : Février 2025

