# 🍽️ RestauSimplon API — Digitalisation des commandes

## 👨‍🍳​👨‍🍳​👨‍🍳​ Auteurs
- Thomas Lefloch
- Jawad Berrhili
- César Gattano
  
## 🌮 Contexte professionnel
Vous êtes développeur·euse backend au sein d’une start‑up tech spécialisée dans les solutions métier.
Votre nouveau client, RestauSimplon, souhaite digitaliser la gestion de ses commandes.
Aujourd’hui, tout se fait sur papier : erreurs fréquentes et temps de traitement élevés.
Votre mission consiste à réaliser une API REST complète sous FastAPI pour gérer les articles du menu, les clients et les commandes, tout en intégrant :
- Authentification/Autorisation par jetons (JWT).
- Conteneurisation via Docker & Docker Compose.
- CI/CD & tests automatisés (GitHub Actions ou GitLab CI, pytest).

## 🥗 Présentation des fonctionnalités
- Gestion des **articles du menu** (CRUD)
- Gestion des **clients** (CRUD)
- Gestion des **commandes** avec suivi du statut au fur et à mesure du traitement
- **Authentification & Autorisation** à l'aide de jetons JWT
- **Conteneurisation** avec Docker et Docker Compose

## 🍛 Stack technique
- **Langage** : Python 3.12
- **Framework** : FastAPI
- **ORM** : SQLModel
- **Base de données** : PostgreSQL
- **Migrations BDD** : Alembic
- **Authentification & Autorisation** : OAuth2 Password avec access & refresh tokens JWT 
- **Conteneurisation** : Docker & Docker Compose

## 🍔 Installation & Utilisation

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

### Variables d'environnement
Les variables d'environnement sont décrites dans le fichier [.env.example](.env.example)

### 4️⃣ Lancer l'application (local)
```bash
# Avec fastapi
fastapi dev app/main.py

# Avec uvicorn
uvicorn app.main:app --port 8000
```
API disponible sur [http://localhost:8000](http://localhost:8000)  
Documentation interactive : [Swagger UI](http://localhost:8000/docs)  
Documentation interactive : [OpenAPI UI](http://localhost:8000/redoc)

### 5️⃣ Construire la base de donnée
```sh
alembic upgrade head
```

### 6️⃣ Insérer les données de tests
```sh
python app/database.py
```
N'oubliez pas les variables d'environnement:
- ADMIN_EMAIL
- ADMIN_PASSWORD
Elles servent à définir l'utilisateur admin pour les données de tests

## 🍝 Dockerisation
### Lancer l'application avec Docker Compose
/!\ ne pas oublier les variables d'environnement

```bash
docker compose -f compose.test.yaml up
```

Cela lancera :
- La base PostgreSQL
- L'éxecution des migrations de la base
- L'API

Pour lancer l'environnement production
```bash
docker compose -f compose.prod.yaml up
```

## 🥘 Lancement des tests

## 🥙 CI/CD


## 🍕 Arborescence du projet

## 🥤 Licence
Ce projet est sous licence MIT — voir le fichier [LICENSE](LICENSE) pour plus d'informations.
