# ScrumForge

Le projet **ScrumForge** offre un espace où chaque inscrit peut travailler ses compétences pour réussir les certifications Scrum.org. Grâce à un entraînement progressif, les utilisateurs se préparent en toute confiance à passer ces certifications.

---

## Architecture du Projet

Le projet est composé de plusieurs applications Django, chacune responsable d'un domaine fonctionnel spécifique :

- **Authentication**  
  Gère l'authentification via JWT, la réinitialisation de mot de passe et l'authentification sociale (Google, LinkedIn). Cette application se concentre exclusivement sur la gestion des sessions et des tokens.

- **User Management**  
  Est dédiée au CRUD complet des utilisateurs : inscription, consultation, mise à jour et suppression des comptes. Cette application offre des endpoints distincts pour les utilisateurs eux-mêmes et pour les administrateurs.

- **Certifications & Compétences**  
  Fournit des endpoints pour créer, lister, afficher, mettre à jour et supprimer des certifications, ainsi que pour gérer les compétences associées à chaque certification.

- **Dashboard** (optionnel)  
  Offre une vue d'ensemble destinée aux utilisateurs authentifiés.

---

## 🏠 Backend

### 📌 Authentication API

L'application **Authentication** (accessible via `/authentication/`) se charge de :

- **Connexion (JWT)**  
  - **Méthode** : `POST`  
  - **URL** : `/authentication/token/`  
  - **Description** : Retourne un `access` et un `refresh` token en cas de succès.  
  - **Exemple de requête** :
    ```json
    {
      "username": "john_doe",
      "password": "SecurePass123!"
    }
    ```
  - **Exemple de réponse** :
    ```json
    {
      "access": "jwt_access_token",
      "refresh": "jwt_refresh_token"
    }
    ```

- **Rafraîchissement du Token JWT**  
  - **Méthode** : `POST`  
  - **URL** : `/authentication/token/refresh/`

- **Déconnexion**  
  - **Méthode** : `POST`  
  - **URL** : `/authentication/logout/`  
  - **Exemple de requête** :
    ```json
    {
      "refresh": "jwt_refresh_token"
    }
    ```

- **Réinitialisation du Mot de Passe**  
  - **Méthode** : `POST`  
  - **URL** : `/authentication/reset-password/`  
  - **Exemple de requête** :
    ```json
    {
      "email": "john@example.com"
    }
    ```
  - **Exemple de réponse** (en mode DEBUG, le nouveau mot de passe est inclus) :
    ```json
    {
      "message": "Un nouveau mot de passe a été envoyé.",
      "username": "john_doe",
      "new_password": "GeneratedPass123"
    }
    ```

---

### 👥 User Management API

L'application **User Management** (accessible via `/user-management/`) prend en charge le CRUD des utilisateurs :

- **Inscription / Création d'un Utilisateur**  
  - **Méthode** : `POST`  
  - **URL** : `/user-management/register/`  

- **Liste des Utilisateurs** (admin uniquement)  
  - **Méthode** : `GET`  
  - **URL** : `/user-management/users/`  

- **Détail d'un Utilisateur** (admin uniquement)  
  - **Méthode** : `GET`  
  - **URL** : `/user-management/users/<id>/`  

- **Mise à jour du Profil Utilisateur**  
  - **Méthode** : `PATCH`  
  - **URL** : `/user-management/users/self/`  

- **Suppression d'un Utilisateur** (admin uniquement)  
  - **Méthode** : `DELETE`  
  - **URL** : `/user-management/users/<id>/delete/`  

---

### 🔹 Certification & Compétences API

Les endpoints liés aux certifications se trouvent sous `/certifications/` et incluent :

1. **Création d'une Certification (Admin)**
   - **Méthode** : `POST`
   - **URL** : `/certifications/`

2. **Liste des Certifications**
   - **Méthode** : `GET`
   - **URL** : `/certifications/`

3. **Détail d'une Certification (avec compétences)**
   - **Méthode** : `GET`
   - **URL** : `/certifications/<id>/`

4. **Mise à jour d'une Certification (Admin)**
   - **Méthode** : `PATCH` ou `PUT`
   - **URL** : `/certifications/<id>/`

5. **Suppression d'une Certification (Admin)**
   - **Méthode** : `DELETE`
   - **URL** : `/certifications/<id>/`

---

### 🔒 Sécurité

- **JWT** : utilisé pour l'authentification dans les applications Authentication et User Management.
- **OAuth2** : utilisé pour l'authentification sociale (Google, LinkedIn).
- **Permissions Avancées** :
  - **Utilisateur** : Doit être authentifié pour consulter certaines informations.
  - **Administrateur** : Requis pour les opérations sensibles (création, mise à jour, suppression) dans User Management et Certifications.

---

📊 **Auteur** : Garance Richard  
📧 **Contact** : garance.richard@gmail.com  
🗓 **Dernière mise à jour** : [Date actuelle]  

