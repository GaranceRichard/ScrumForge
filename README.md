# ScrumForge

Le projet **ScrumForge** vise à proposer un espace où chaque inscrit peut travailler ses compétences sur les certifications Scrum.org et, grâce à un entraînement progressif, se préparer en toute confiance à passer ces certifications.

---

## 🏰 Backend

### 📌 Authentication API

L'API **Authentication** est un service développé avec **Django Rest Framework (DRF)** qui gère :
- L'**authentification JWT**
- La gestion des **utilisateurs**
- L'**authentification sociale** (Google, LinkedIn)
- L'administration sécurisée avec des **permissions avancées**

### 💁 Structure du projet

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

### 🔹 Endpoints de l'Authentication API

Tous les endpoints d'authentification sont accessibles via `/authentication/`.

#### 1. Inscription  
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

#### 2. Connexion (JWT)  
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

#### 3. Rafraîchir le Token JWT  
- **Méthode** : `POST`  
- **URL** : `/authentication/token/refresh/`

#### 4. Déconnexion  
- **Méthode** : `POST`  
- **URL** : `/authentication/logout/`  
```json
{
  "refresh": "jwt_refresh_token"
}
```

#### 5. Profil utilisateur  
- **Méthode** : `GET`  
- **URL** : `/authentication/users/me/`

#### 6. Mise à jour du profil (Utilisateur)  
- **Méthode** : `PATCH`  
- **URL** : `/authentication/users/self-update/`

#### 7. Mise à jour d'un utilisateur (Admin)  
- **Méthode** : `PATCH`  
- **URL** : `/authentication/users/<user_id>/update/`

#### 8. Suppression du compte (Admin)  
- **Méthode** : `DELETE`  
- **URL** : `/authentication/users/<user_id>/delete/`

---

### 🔹 Certification & Compétences API

Les endpoints liés aux certifications sont accessibles via `/certifications/`.

1. **Création d'une certification (Admin)**
   - **Méthode** : `POST`
   - **URL** : `/certifications/`
   - **Description** : Permet à un administrateur de créer une certification.

2. **Liste des certifications**
   - **Méthode** : `GET`
   - **URL** : `/certifications/`
   - **Description** : Retourne la liste des certifications existantes.

3. **Détail d'une certification (avec compétences rattachées)**
   - **Méthode** : `GET`
   - **URL** : `/certifications/<id>/`
   - **Description** : Affiche les détails d'une certification, incluant la liste des compétences associées.

4. **Mise à jour d'une certification (Admin)**
   - **Méthode** : `PATCH` (ou `PUT`)
   - **URL** : `/certifications/<id>/`
   - **Description** : Permet à un administrateur de mettre à jour le nom, la description et le logo d'une certification.

5. **Suppression d'une certification (Admin)**
   - **Méthode** : `DELETE`
   - **URL** : `/certifications/<id>/`
   - **Description** : Permet à un administrateur de supprimer une certification.

---

### 🔒 Sécurité

- **JWT** : utilisé pour l'authentification.
- **OAuth2** : pour l'authentification sociale (Google, LinkedIn).
- **Rôles et permissions avancées** :
  - **Utilisateur** : doit être authentifié pour consulter les endpoints (GET).
  - **Administrateur** : requis pour les opérations de création, mise à jour et suppression.

---

📈 **Auteur** : Garance Richard  
📧 **Contact** : garance.richard@gmail.com  
🗓 **Dernière mise à jour** : Février 2025
