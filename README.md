# ScrumForge – Plateforme de préparation aux certifications Scrum.org

Le projet **ScrumForge** offre un espace où chaque inscrit peut travailler ses compétences pour réussir les certifications Scrum.org. Grâce à un entraînement progressif, les utilisateurs se préparent en toute confiance à passer ces certifications.
C'est un projet fullstack conçu par **Garance Richard**, Delivery Manager / Coach Agile, pour entraîner les utilisateurs aux certifications agiles Scrum.org via une approche par compétences, référentiels et rôles.

---

## 🎯 Objectif

ScrumForge vise à offrir une **expérience d’apprentissage ciblée** et mesurable pour les certifications Scrum (PSM, PSPO, PSU, PAL, etc.) :

- Alignement sur les **compétences évaluées par Scrum.org**
- Architecture sécurisée, **scalable et modulaire**
- Utilisation de **standards techniques robustes** (JWT, DRF, React, PostgreSQL)

---

## ⚙️ Stack Technique

| Couche         | Technologies                                  |
|----------------|-----------------------------------------------|
| Frontend       | React + TailwindCSS                           |
| Backend        | Django 5 + Django Rest Framework              |
| Authentification | JWT (rotation, refresh), OAuth2             |
| Base de données| SQLite (dev), PostgreSQL (production-ready)   |
| Documentation API | OpenAPI 3 – Swagger + ReDoc                |

---

## 🚧 Roadmap produit

- [ ] Mise en place CI/CD (GitHub Actions)
- [ ] Intégration scoring utilisateur & indicateurs (cycle time, taux de bonnes réponses)
- [ ] Version SaaS déployée sur Railway / Render
- [ ] Ajout d’une interface admin analytics

---

# ScrumForge


---

## Architecture modulaire du Projet

Le projet est composé de plusieurs applications Django, chacune responsable d'un domaine fonctionnel spécifique :

- **Authentication**  
  Gère l'authentification via JWT, la réinitialisation de mot de passe et l'authentification sociale (Google, LinkedIn). Cette application se concentre exclusivement sur la gestion des sessions et des tokens.
  - JWT sécurisé avec refresh token, rotation, blacklist
  - Endpoints de login / logout / reset password
  - Backend extensible avec support futur OAuth2 (Google, LinkedIn)

- **User Management**  
  Est dédiée au CRUD complet des utilisateurs : inscription, consultation, mise à jour et suppression des comptes. Cette application offre des endpoints distincts pour les utilisateurs eux-mêmes et pour les administrateurs.
  - Modèle `CustomUser` (admin / user)
  - Création, mise à jour, suppression de comptes
  - Séparation des droits + endpoints protégés

- **Certifications & Compétences**  
  Fournit des endpoints pour créer, lister, afficher, mettre à jour et supprimer des certifications, ainsi que pour gérer les compétences associées à chaque certification.
  - Référentiels modélisés : PSM, PSPO, PSU, PAL, SPS, PSK…
  - Chaque certification est liée à un set de compétences (4–5 par référentiel)
  - Préparation ciblée par objectif de progression

- **Dashboard** (optionnel)  
  Offre une vue d'ensemble destinée aux utilisateurs authentifiés.
  - (À venir) Visualisation des progrès
  - Objectif : offrir un feedback adaptatif sur les performances

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

