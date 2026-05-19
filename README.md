# 🚀 API de Prédiction d'Attrition des Employés

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)
[![Hugging Face](https://img.shields.io/badge/Deploy-Hugging%20Face-yellow.svg)](https://huggingface.co/spaces)
[![NeonDB](https://img.shields.io/badge/Database-NeonDB-green.svg)](https://neon.tech/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Une API REST complète pour prédire l'attrition des employés à l'aide du Machine Learning.  
Elle est construite avec **FastAPI**, **NeonDB PostgreSQL**, **SQLAlchemy** et des modèles **scikit-learn**, puis déployable sur **Hugging Face Spaces** via Docker.

🔗 **API Live** : [Accéder à l'API](https://lealjo27-attrition-api.hf.space/docs)

---

## 📋 Table des matières

- [🎯 Aperçu](#-aperçu)
- [✨ Fonctionnalités](#-fonctionnalités)
- [🏗️ Architecture](#️-architecture)
- [📦 Installation locale](#-installation-locale)
- [⚙️ Configuration](#️-configuration)
- [📡 API Endpoints](#-api-endpoints)
- [🧪 Tests](#-tests)
- [🐳 Docker](#-docker)
- [🚀 Déploiement Hugging Face](#-déploiement-hugging-face)
- [💻 Utilisation](#-utilisation)
- [📊 Base de données](#-base-de-données)
- [🔐 Sécurité](#-sécurité)
- [📚 Structure du projet](#-structure-du-projet)
- [🛠️ Technologies utilisées](#️-technologies-utilisées)
- [📄 Licence](#-licence)
- [👤 Auteur](#-auteur)

---

## 🎯 Aperçu

Cette API prédit le risque d'attrition, c'est-à-dire le risque de départ d'un employé, à partir de ses données professionnelles et personnelles.

Le modèle de Machine Learning entraîné avec **scikit-learn** est sérialisé avec **joblib** et chargé par l'API pour réaliser des prédictions en temps réel.

### 🎓 Cas d'usage

- 📊 Prédire les employés à risque de départ
- 🎯 Identifier les principaux facteurs influençant l'attrition
- 📈 Surveiller les tendances d'attrition dans l'entreprise
- 🔔 Alerter les équipes RH pour mettre en place des actions préventives

---

## ✨ Fonctionnalités

- ✅ Prédiction d'attrition en temps réel avec probabilité
- ✅ Authentification sécurisée par JWT
- ✅ API REST documentée automatiquement avec Swagger/OpenAPI
- ✅ Historique des prédictions sauvegardé en base de données
- ✅ Logging des appels API
- ✅ Tests unitaires avec `pytest`
- ✅ Gestion d'erreurs claire et robuste
- ✅ Conteneurisation avec Docker
- ✅ Persistance des données avec NeonDB PostgreSQL

---

## 🏗️ Architecture

```text
Projet5_new/
├── main.py                         # Application FastAPI
├── auth.py                         # Authentification JWT
├── requirements.txt                # Dépendances Python
├── Dockerfile                      # Image Docker
├── docker-compose.yml              # Orchestration Docker
├── .env                            # Exemple de variables d'environnement
├── .github/
│   └── workflows/
│       └── deploy.yml               # CI/CD GitHub Actions
├── database/
│   ├── creation_database.py        # Modèles SQLAlchemy
│   └── modele_attrition.joblib     # Modèle ML pré-entraîné
│   └── data_preparee.csv           # Données concernant les salariés
│   └── import_data.py              # Script import des données
├── tests/
│   └── test_main.py                # Tests unitaires
└── README.md                       # Documentation
```

### Stack technique

| Composant | Technologie |
|---|---|
| Framework | FastAPI |
| Base de données | PostgreSQL / NeonDB |
| ORM | SQLAlchemy |
| Authentification | JWT / PyJWT |
| Modèle ML | scikit-learn |
| Sérialisation modèle | joblib |
| Conteneurisation | Docker / Docker Compose |
| Déploiement | Hugging Face Spaces |
| Tests | pytest |
| CI/CD | GitHub Actions |

---

## 📦 Installation locale

### Prérequis

- Python 3.12+
- Git
- Docker, optionnel
- Un compte NeonDB, optionnel si vous utilisez une base locale

### Étapes

```bash
# 1. Cloner le repository
git clone https://github.com/lealjo27/Projet5_new.git
cd Projet5_new

# 2. Créer un environnement virtuel
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les variables d'environnement
cp .env.example .env

# 5. Démarrer l'application
uvicorn main:app --reload

# 6. Accéder à l'API
# Swagger UI : http://localhost:8000/docs
# ReDoc      : http://localhost:8000/redoc
```

---

## ⚙️ Configuration

Créer un fichier `.env` à la racine du projet.

```env
# Base de données NeonDB
DATABASE_URL=postgresql://user:password@ep-xxxx.eu-west-1.aws.neon.tech/dbname?sslmode=require

# Sécurité JWT
SECRET_KEY=votre-cle-secrete-tres-longue-et-complexe
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Obtenir une `DATABASE_URL` NeonDB

1. Créer un compte sur [https://neon.tech/](https://neon.tech/)
2. Créer un projet PostgreSQL
3. Copier la connection string
4. Ajouter le paramètre SSL si nécessaire :

```env
DATABASE_URL=postgresql://user:password@ep-xxxx.eu-west-1.aws.neon.tech/mydb?sslmode=require
```

---

## 📡 API Endpoints

### 🔓 Racine

```http
GET /
```

#### Réponse

```json
{
  "message": "API attrition active"
}
```

---

### 🔐 Authentification

```http
POST /token
Content-Type: application/x-www-form-urlencoded
```

#### Corps de requête

```text
username=alice&password=secret123
```

#### Réponse

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Utilisateur par défaut

```text
alice / secret123
```

---

### 🎯 Prédiction

Endpoint protégé nécessitant un token JWT.

```http
GET /predict/{id_employe}
Authorization: Bearer {access_token}
```

#### Exemple avec cURL

```bash
curl -X GET "http://localhost:8000/predict/20" \
  -H "Authorization: Bearer votre_token_jwt"
```

#### Réponse réussie `200`

```json
{
  "employe_id": 20,
  "prediction": "Risque de départ",
  "probabilite_depart": 85.0,
  "message": "Il y a 85.0% de risques que cet employé parte.",
  "top_3_facteurs_influence": [
    "Distance domicile travail",
    "Heure supplementaires",
    "Satisfaction employee equilibre pro perso"
  ]
}
```

#### Réponse erreur `404`

```json
{
  "detail": "L'ID 999 n'existe pas en base"
}
```

---

## 🧪 Tests

```bash
# Lancer tous les tests
python -m pytest tests/ -v -s

# Lancer un test spécifique
python -m pytest tests/test_main.py::test_predict_success_with_mock -v -s

# Lancer les tests avec couverture
python -m pytest tests/ --cov=.
```

### Résultats actuels

```text
✅ 5/6 tests réussis
❌ 1 test edge case en cours de correction
```

---

## 🐳 Docker

### Lancer localement avec Docker

```bash
# Construire l'image
docker build -t attrition-api .

# Lancer le conteneur
docker run -p 8000:8000 --env-file .env attrition-api
```

### Lancer avec Docker Compose

```bash
# Lancer API + PostgreSQL
docker-compose up -d

# Arrêter les services
docker-compose down

# Voir les logs
docker-compose logs -f api
```

### Exemple de `docker-compose.yml`

```yaml
version: "3.8"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: attrition_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

---

## 🚀 Déploiement Hugging Face

### Prérequis

- Un compte Hugging Face : [https://huggingface.co/](https://huggingface.co/)
- Un token d'accès Hugging Face : `Settings → Access Tokens`

### 1. Créer un Space Hugging Face

Sur [https://huggingface.co/spaces](https://huggingface.co/spaces), créer un nouveau Space :

```text
Nom       : attrition-api
Owner     : votre username
License   : MIT
Visibility: Public ou Private
SDK       : Docker
```

### 2. Cloner le Space

```bash
git clone https://huggingface.co/spaces/lealjo27/attrition-api
cd attrition-api
```

### 3. Ajouter les fichiers du projet

```bash
cp ../Projet5_new/main.py .
cp ../Projet5_new/auth.py .
cp ../Projet5_new/requirements.txt .
cp ../Projet5_new/Dockerfile .
cp -r ../Projet5_new/database/ .
```

### 4. Configurer les secrets

Dans le Space Hugging Face :

```text
Settings → Repository secrets
```

Ajouter :

```text
DATABASE_URL = postgresql://user:password@ep-xxxx...
SECRET_KEY = votre-cle-secrete
```

### 5. Pousser le code

```bash
git add .
git commit -m "Déploiement initial API attrition"
git push origin main
```

### 6. Accéder à l'API

Après le build, l'API sera disponible à l'adresse :

```text
https://lealjo27-attrition-api.hf.space
```

Endpoints utiles :

```text
Swagger UI : https://lealjo27-attrition-api.hf.space/docs
API        : https://lealjo27-attrition-api.hf.space/predict/20
```

---

## 💻 Utilisation

### Avec Python

```python
import requests

BASE_URL = "https://lealjo27-attrition-api.hf.space"

# 1. Authentification
response = requests.post(
    f"{BASE_URL}/token",
    data={
        "username": "alice",
        "password": "secret123"
    }
)

response.raise_for_status()
token = response.json()["access_token"]

print(f"✅ Token obtenu : {token[:20]}...")

# 2. Faire une prédiction
headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(
    f"{BASE_URL}/predict/20",
    headers=headers
)

response.raise_for_status()
print(response.json())
```

### Avec cURL

```bash
# 1. S'authentifier
TOKEN=$(curl -X POST "https://lealjo27-attrition-api.hf.space/token" \
  -d "username=alice&password=secret123" | jq -r '.access_token')

echo "Token : $TOKEN"

# 2. Faire une prédiction
curl -X GET "https://lealjo27-attrition-api.hf.space/predict/20" \
  -H "Authorization: Bearer $TOKEN"
```

### Avec Swagger UI

1. Accéder à :

```text
https://lealjo27-attrition-api.hf.space/docs
```

2. Cliquer sur **Authorize**
3. Entrer les identifiants ou le token selon la configuration de sécurité
4. Tester les endpoints directement depuis l'interface

---

## 📊 Base de données

### Table `employe`

Contient les données des employés utilisées pour effectuer les prédictions.

```sql
SELECT *
FROM employe
LIMIT 5;
```

### Table `predictions`

Contient l'historique des prédictions effectuées par l'API.

```sql
SELECT employe_id, prediction, proba, facteurs, date_prediction
FROM predictions
ORDER BY date_prediction DESC
LIMIT 10;
```

### Table `logs`

Contient les logs d'exécution des appels API.

```sql
SELECT id_prediction, temps_execution, date_prediction
FROM logs
ORDER BY date_prediction DESC
LIMIT 10;
```

---

## 🔐 Sécurité

- ✅ Authentification par JWT
- ✅ Chiffrement HTTPS via Hugging Face et NeonDB
- ✅ Variables sensibles stockées dans les secrets Hugging Face
- ✅ Validation des entrées côté API
- ✅ Logging des appels pour audit et traçabilité
- ✅ Gestion claire des erreurs HTTP

> ⚠️ Recommandation : ne pas conserver d'identifiants par défaut en production.  
> Remplacer `alice / secret123` par un système utilisateur sécurisé ou une gestion d'accès dédiée.

---

## 📚 Structure du projet

| Fichier | Rôle |
|---|---|
| `main.py` | Application FastAPI principale |
| `auth.py` | Gestion de l'authentification JWT |
| `database/creation_database.py` | Modèles SQLAlchemy |
| `database/modele_attrition.joblib` | Modèle ML sérialisé |
| `requirements.txt` | Dépendances Python |
| `Dockerfile` | Image Docker de l'application |
| `docker-compose.yml` | Orchestration locale API + base de données |
| `tests/test_main.py` | Suite de tests unitaires |
| `.env.example` | Template de configuration |
| `.github/workflows/tests.yml` | Pipeline CI/CD GitHub Actions |

---

## 🛠️ Technologies utilisées

```text
FastAPI 0.104+      - Framework web asynchrone
SQLAlchemy 2.0+     - ORM Python
NeonDB              - PostgreSQL serverless
PyJWT 2.8+          - Authentification JWT
scikit-learn        - Modèles Machine Learning
joblib              - Sérialisation du modèle
pytest              - Framework de tests
Docker              - Conteneurisation
Hugging Face Spaces - Plateforme de déploiement
```

---

## 📄 Licence

Ce projet est sous licence MIT.  
Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👤 Auteur

**Jo** — [@lealjo27](https://github.com/lealjo27)

- 📧 Email : lealjo27@gmail.com
- 🐙 GitHub : [https://github.com/lealjo27](https://github.com/lealjo27)

---

**Version :** 1.1.0  
**Statut :** ✅ Production Ready  
**Dernière mise à jour :** 2026-05-19