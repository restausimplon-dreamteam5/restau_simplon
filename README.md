# 🍽️ RestauSimplon API — Digitalisation des commandes

## 👨‍💻 Auteurs
- Thomas Lefloch
- Jawad Berrhili
- César Gattano
  
## 📌 Contexte professionnel
**RestauSimplon**, un restaurant en pleine modernisation, souhaite digitaliser la gestion de ses commandes pour éviter les erreurs de communication et accélérer leur traitement.

En tant que développeurs backend, notre mission a été de concevoir une **API REST complète sous FastAPI** permettant de gérer les articles du menu, les clients et les commandes. Une fois développé, l'application et sa base de données ont été conteneurisées puis un processus CI/CD incluant des pipelines de tests ont été mis en place.

## 🚀 Présentation des fonctionnalités
- Gestion des **articles du menu** (CRUD)
- Gestion des **clients** (CRUD)
- Gestion des **commandes** avec suivi du statut au fur et à mesure du traitement
- **Authentification & Autorisation** à l'aide de jetons JWT
- **Conteneurisation** avec Docker et Docker Compose
- **Tests automatisés** avec pytest
- **CI/CD** via GitHub Actions

## 🛠 Stack technique
- **Langage** : Python 3.12
- **Framework** : FastAPI
- **ORM** : SQLModel
- **Base de données** : PostgreSQL
- **Migrations BDD** : Alembic
- **Authentification & Autorisation** : OAuth2 Password avec access & refresh tokens JWT 
- **Conteneurisation** : Docker & Docker Compose
- **Tests** : pytest
- **CI/CD** : GitHub Actions

## 📦 Installation & Utilisation

### 1️⃣ Cloner le dépôt
```bash
git clone git@github.com:restausimplon-dreamteam5/restau_simplon.git
cd restau_simplon
```

### 2️⃣ Créer et activer un environnement virtuel
```bash
python -m venv .venv
source .venv/bin/activate  # sous Linux/Mac
.venv\Scripts\activate   # sous Windows
```

### 3️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4️⃣ Lancer l'application (local)
```bash
fastapi dev app/main.py
```

API disponible sur [http://localhost:8000](http://localhost:8000)  
Documentation interactive : [Swagger UI](http://localhost:8000/docs)  
Documentation interactive : [OpenAPI UI](http://localhost:8000/redoc)

## 🐳 Dockerisation
### Lancer l'application avec Docker Compose
```bash
docker-compose up --build
```

Cela lancera :
- La base PostgreSQL
- L'éxecution des migrations de la base
- L'API

## 🧪 Lancement des tests
```bash
pytest
```

## 🔄 CI/CD
Un pipeline **GitHub Actions** est configuré pour :
- Installer les dépendances
- Lancer les tests unitaires
- Construire et publier l'image Docker

## Arborescence du projet

## 💡 Résumé des points forts
- API REST complète avec **sécurité intégrée**
- **Scalable** et **prête pour la production**
- **Conteneurisation** facilitant le déploiement
- **Automatisation** avec CI/CD

## 📄 Licence
Ce projet est sous licence MIT — voir le fichier [LICENSE](LICENSE) pour plus d'informations.
