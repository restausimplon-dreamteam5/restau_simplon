# 🍽️ RestauSimplon API — Digitalisation des commandes

## 👨‍🍳​👨‍🍳​👨‍🍳​ Auteurs
- Thomas Lefloch
- Jawad Berrhili
- César Gattano

## 🌮 Contexte professionnel
Vous êtes développeur·euse backend au sein d’une start‑up tech spécialisée dans les solutions métier.
Votre nouveau client, **RestauSimplon**, souhaite digitaliser la gestion de ses commandes.
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
- **Intégration continue** avec GitHub Actions (qualité de code, tests unitaires et d'intégration)

## 🍛 Stack technique
- **Langage** : Python 3.12
- **Framework** : FastAPI
- **ORM** : SQLModel
- **Base de données** : PostgreSQL
- **Migrations BDD** : Alembic
- **Authentification & Autorisation** : OAuth2 Password avec access & refresh tokens JWT
- **Conteneurisation** : Docker & Docker Compose
- **Tests unitaires** : Pytest
- **Tests d'intégration**: Pytest via requests
- **CI/CD** : GitHub Actions

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

### 4️⃣ Variables d'environnement
Les variables d'environnement sont décrites dans le fichier [.env.example](.env.example)

### 5️⃣ Lancer l'application (local)
```bash
# Avec fastapi
fastapi dev app/main.py

# Avec uvicorn
uvicorn app.main:app --port 8000
```
API disponible sur [http://localhost:8000](http://localhost:8000)  
Documentation interactive : [Swagger UI](http://localhost:8000/docs)  
Documentation interactive : [OpenAPI UI](http://localhost:8000/redoc)

### 6️⃣ Construire la base de données
```sh
alembic upgrade head
```

### 7️⃣​ Insérer les données de tests
```sh
python app/database.py
```
Pour cette étape, n'oubliez pas les variables d'environnement:
- **ADMIN_EMAIL**
- **ADMIN_PASSWORD**
Elles servent à définir l'utilisateur *admin* pour les données de tests

## 🍝 Dockerisation
### Lancer l'application avec Docker Compose
⚠️​ Ne pas oublier la mise en place des variables d'environnement ⚠️​

```bash
docker compose -f compose.test.yaml up --build
```
*Si les droits superutilisateur sont requis, faire précéder la commande de **sudo***

Cette commande lancera :
- La base PostgreSQL
- L'éxecution des migrations de la base
- L'API

***Alternative:*** Pour que la base de données contiennent des données de test:

```bash
docker compose -f compose.test.yaml --profile data up --build
```

***Alternative:*** Pour lancer l'environnement *production*
```bash
docker compose -f compose.prod.yaml up
```

## 🥘 Lancement des tests

Une fois l'application lancée, les tests unitaires peuvent être lancée:

```bash
pytest tests/units
```

puis les test d'intégration

```bash
pytest tests/intégrations
```

## 🥙 CI/CD


## 🍕 Arborescence du projet

```bash
├── app # --------------- Dossier principal
│   ├── models # -------- Modèles pour la base de données
│   │   └── models.py
│   ├── schemas # ------- Schémas de validation/filtre des données
│   │   └── schemas.py
│   ├── crud # ---------- Fonctionnalités CRUD
│   │   ├── menu_items.py
│   │   ├── order.py
│   │   └── user_info.py
│   ├── routes # -------- Routes FastAPI
│   │   ├── login.py
│   │   ├── menu_item.py
│   │   ├── order.py
│   │   ├── roles.py
│   │   └── user.py
│   ├── database.py # --- Mise en base de données de test
│   ├── deps.py # ------- Dépendances de l'API
│   ├── main.py
│   │
│   ├── menu_items.json # Données de tests générées par IA
│   └── users_info.json
│ 
├── conception # -------- Documentations initiales
│   ├── dictionnaire_donnee.md
│   ├── fichier_source_jmerise
│   ├── mcd_restausimplon.png
│   └── mld_restausimplon.png
│ 
├── migrations # -------- Scripts des migrations de la BDD
│   ├── versions
│   │   └── ...
│   ├── env.py # -------- Fichiers de configuration d'Alembic
│   ├── script.py.mako
│   └── README
│
├── tests
│   ├── units # --------- Collection des tests unitaires
│   │   └── schemas
│   │       └── ...
│   └── integrations # -- Collection des tests d'intégration
│       └── ...      #    (test des routes)
│ 
├── .github # ----------- CI/CD Github Actions
│   └── workflows
│       ├── on_pr_dev.yaml
│       └── on_push.yaml
│
│ # --------------------- Configurations
├── alembic.ini
├── requirements.txt
│ # --------------------- Conteneurisation
├── app.Dockerfile
├── migration.Dockerfile
├── compose.prod.yaml
├── compose.test.yaml
│ # --------------------- Docs
├── README.md # --------- Documentation générale
├── .env.example # ------ Template pour le fichier .env
├── docker.md # --------- Mémo commande docker
└── LICENSE
```

## 🥤 Licence
Ce projet est sous licence MIT — voir le fichier [LICENSE](LICENSE) pour plus d'informations.
