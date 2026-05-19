# 🚀 API Prédiction d'Attrition des Employés

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)
[![Hugging Face](https://img.shields.io/badge/Deploy-Hugging%20Face-yellow.svg)](https://huggingface.co/spaces)
[![NeonDB](https://img.shields.io/badge/Database-NeonDB-green.svg)](https://neon.tech/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Une API REST complète pour prédire l'attrition des employés en utilisant le Machine Learning. Construite avec **FastAPI**, **NeonDB (PostgreSQL)**, et des modèles **scikit-learn**. Déployée sur **Hugging Face Spaces**.

🔗 **API Live** : [Accédez à l'API](https://lealjo27-projet5-attrition-api.hf.space/docs)

---

## 📋 Table des matières

- [Aperçu](#aperçu)
- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Tests](#tests)
- [Docker](#docker)
- [Déploiement Hugging Face](#déploiement-hugging-face)
- [Utilisation](#utilisation)

---

## 🎯 Aperçu

Cette API prédit le risque d'attrition (départ) d'un employé en fonction de ses données professionnelles et personnelles. Le modèle ML entraîné (scikit-learn) est sérialisé avec **joblib** et s'exécute en temps réel pour chaque prédiction.

### 🎓 Cas d'usage
- 📊 Prédire les employés à risque de départ
- 🎯 Identifier les 3 facteurs principaux influençant l'attrition
- 📈 Surveiller les tendances d'attrition dans l'entreprise
- 🔔 Alerter les RH pour des interventions préventives

---

## ✨ Fonctionnalités

- ✅ **Prédiction d'attrition** en temps réel avec probabilité
- ✅ **Authentification JWT** sécurisée
- ✅ **API REST** documentée avec Swagger
- ✅ **Historique des prédictions** sauvegardé en BDD
- ✅ **Logging complet** des appels API
- ✅ **Tests unitaires** exhaustifs (5/6 tests ✓)
- ✅ **Gestion d'erreurs** robuste et détaillée
- ✅ **Docker** pour déploiement facile
- ✅ **NeonDB** pour persistance des données

---

## 🏗️ Architecture

Projet5_new/ ├── main.py # Application FastAPI ├── auth.py # Authentification JWT ├── requirements.txt # Dépendances ├── Dockerfile # Image Docker ├── docker-compose.yml # Orchestration Docker ├── .env.example # Variables d'environnement ├── .github/ │ └── workflows/ │ └── tests.yml # CI/CD GitHub Actions ├── database/ │ ├── creation_database.py # Modèles SQLAlchemy │ └── modele_attrition.joblib # Modèle ML préentraîné ├── tests/ │ └── test_main.py # Tests unitaires └── README.md # Documentation

Code

### Stack Technique

| Composant | Technologie |
|-----------|-------------|
| **Framework** | FastAPI |
| **Base de données** | PostgreSQL (NeonDB) |
| **ORM** | SQLAlchemy |
| **Auth** | JWT (PyJWT) |
| **ML Model** | scikit-learn (joblib) |
| **Conteneurisation** | Docker + Docker Compose |
| **Déploiement** | Hugging Face Spaces |
| **Tests** | pytest |
| **CI/CD** | GitHub Actions |

---

## 📦 Installation locale

### Prérequis
- Python 3.12+
- Docker (optionnel)
- Git

### Étapes

```bash
# 1. Cloner le repository
git clone https://github.com/lealjo27/Projet5_new.git
cd Projet5_new

# 2. Créer environnement virtuel
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# ou
.venv\Scripts\activate  # Windows

# 3. Installer dépendances
pip install -r requirements.txt

# 4. Configurer variables d'environnement
cp .env.example .env
# Éditer .env avec vos paramètres

# 5. Démarrer l'application
uvicorn main:app --reload

# 6. Accéder à l'API
# Swagger UI : http://localhost:8000/docs
# ReDoc : http://localhost:8000/redoc
⚙️ Configuration
Fichier .env
env
# Base de données NeonDB
DATABASE_URL=postgresql://user:password@ep-xxxx.eu-west-1.aws.neon.tech/dbname

# Sécurité JWT
SECRET_KEY=votre-clé-secrète-très-longue-et-complexe-ici
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
Obtenir DATABASE_URL de NeonDB
Créer un compte sur https://neon.tech/
Créer un projet PostgreSQL
Copier la connection string
Ajouter dans .env avec le paramètre ?sslmode=require
env
DATABASE_URL=postgresql://user:password@ep-xxxx.eu-west-1.aws.neon.tech/mydb?sslmode=require
📡 API Endpoints
🔓 Racine
HTTP
GET /
Réponse :

JSON
{
  "message": "API attrition active"
}
🔐 Authentification
HTTP
POST /token
Content-Type: application/x-www-form-urlencoded

username=alice&password=secret123
Réponse :

JSON
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
Utilisateurs par défaut :

alice / secret123
🎯 Prédiction (Nécessite authentification)
HTTP
GET /predict/{id_employe}
Authorization: Bearer {access_token}
Exemple de requête :

bash
curl -X GET "http://localhost:8000/predict/20" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
Réponse réussie (200) :

JSON
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
Réponse erreur (404) :

JSON
{
  "detail": "L'ID 999 n'existe pas en base"
}
🧪 Tests
bash
# Lancer tous les tests
python -m pytest tests/ -v -s

# Lancer un test spécifique
python -m pytest tests/test_main.py::test_predict_success_with_mock -v -s

# Avec coverage
python -m pytest tests/ --cov=.
Résultats actuels
✅ 5/6 tests réussis
❌ 1 test (edge case) en cours de correction
🐳 Docker
Lancer localement avec Docker
bash
# Build l'image
docker build -t attrition-api .

# Lancer le conteneur
docker run -p 8000:8000 --env-file .env attrition-api
Avec Docker Compose
bash
# Lancer API + PostgreSQL
docker-compose up -d

# Arrêter les services
docker-compose down

# Voir les logs
docker-compose logs -f api
Fichier docker-compose.yml :

YAML
version: '3.8'

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
      POSTGRES_USER: xxxxx
      POSTGRES_PASSWORD: xxxxxx
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
🚀 Déploiement Hugging Face
Prérequis
Compte Hugging Face : https://huggingface.co/
Token d'accès HF (Settings → Access Tokens)
Étapes de déploiement
1. Créer un Space sur Hugging Face
bash
# Aller sur https://huggingface.co/spaces
# Créer un nouveau Space :
# - Nom : attrition-api
# - Owner : Votre username
# - License : MIT
# - Private : Non
# - Space SDK : Docker
2. Cloner le Space
bash
git clone https://huggingface.co/spaces/lealjo27/attrition-api
cd attrition-api
3. Ajouter vos fichiers
bash
# Copier vos fichiers du projet
cp ../Projet5_new/main.py .
cp ../Projet5_new/auth.py .
cp ../Projet5_new/requirements.txt .
cp ../Projet5_new/Dockerfile .
cp ../Projet5_new/database/ . -r
4. Configurer les secrets
Sur la page du Space → Settings → Repository secrets :

Code
DATABASE_URL = postgresql://user:password@ep-xxxx...
SECRET_KEY = votre-clé-secrète-ici
5. Pousser le code
bash
git add .
git commit -m "Déploiement initial API attrition"
git push origin main
6. Attendre le déploiement
L'API sera disponible à :

Code
https://lealjo27-attrition-api.hf.space
Endpoints :

Swagger UI : https://lealjo27-attrition-api.hf.space/docs
API : https://lealjo27-attrition-api.hf.space/predict/20
💻 Utilisation
Avec Python
Python
import requests

BASE_URL = "https://lealjo27-attrition-api.hf.space"

# 1. Authentification
response = requests.post(
    f"{BASE_URL}/token",
    data={"username": "alice", "password": "secret123"}
)
token = response.json()["access_token"]
print(f"✅ Token obtenu : {token[:20]}...")

# 2. Faire une prédiction
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    f"{BASE_URL}/predict/20",
    headers=headers
)

print(response.json())
Avec cURL
bash
# 1. S'authentifier
TOKEN=$(curl -X POST "https://lealjo27-attrition-api.hf.space/token" \
  -d "username=alice&password=secret123" | jq -r '.access_token')

echo "Token : $TOKEN"

# 2. Faire une prédiction
curl -X GET "https://lealjo27-attrition-api.hf.space/predict/20" \
  -H "Authorization: Bearer $TOKEN"
Avec Swagger UI
Accédez à : https://lealjo27-attrition-api.hf.space/docs
Cliquez sur "Authorize" et entrez les credentials
Testez les endpoints directement dans l'interface
📊 Base de données
Tables NeonDB
Employe - Données des employés

SQL
SELECT * FROM employe LIMIT 5;
Predictions - Historique des prédictions

SQL
SELECT employe_id, prediction, proba, facteurs, date_prediction 
FROM predictions 
ORDER BY date_prediction DESC 
LIMIT 10;
Logs - Logs des appels API

SQL
SELECT id_prediction, temps_execution, date_prediction 
FROM logs 
ORDER BY date_prediction DESC 
LIMIT 10;
🔐 Sécurité
✅ JWT : Authentification par token
✅ HTTPS : Chiffrage en transit (HF + NeonDB)
✅ Variables secrètes : Stockées dans HF Secrets
✅ Logging : Traçabilité complète
✅ Validation : Input validation sur tous les endpoints
📚 Structure du projet
Fichier	Rôle
main.py	Application FastAPI principale
auth.py	Gestion JWT et authentification
database/creation_database.py	Modèles SQLAlchemy
database/modele_attrition.joblib	Modèle ML sérialisé
requirements.txt	Dépendances Python
Dockerfile	Image Docker optimisée
docker-compose.yml	Orchestration locale
tests/test_main.py	Suite de tests
.env.example	Template configuration
🛠️ Technologies utilisées
Code
FastAPI 0.104+      - Framework web asynchrone
SQLAlchemy 2.0+     - ORM Python
NeonDB              - PostgreSQL serverless
PyJWT 2.8+          - Authentification JWT
scikit-learn        - Modèles ML
joblib              - Sérialisation modèle
pytest              - Framework de tests
Docker              - Conteneurisation
Hugging Face        - Plateforme de déploiement
🚀 Prochaines étapes
 Ajouter metrics (Prometheus)
 Améliorer le modèle ML
 Ajouter caching Redis
 Impl webiste frontend
 Monitoring temps réel
🤝 Contribution
Les contributions sont bienvenues !

bash
# Créer une branche
git checkout -b feature/ma-feature

# Committer
git commit -m "Ajout ma-feature"

# Pousser
git push origin feature/ma-feature

# Créer une Pull Request
📄 License
Ce projet est sous License MIT - Voir LICENSE pour plus de détails.

👤 Auteur
Jo - @lealjo27

📧 Email : lealjo27@gmail.com
🐙 GitHub : https://github.com/lealjo27
💼 LinkedIn : https://www.linkedin.com/in/jonathanfillon/

📖 Ressources
FastAPI Documentation
NeonDB Documentation
Hugging Face Spaces
SQLAlchemy ORM
JWT Documentation
scikit-learn Models
