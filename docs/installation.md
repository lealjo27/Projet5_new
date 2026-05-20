# 📦 Installation locale

## Prérequis

Avant de démarrer, assurez-vous d'avoir installé :

- Python 3.12 ou supérieur
- Git
- Docker, optionnel
- Un compte NeonDB, optionnel si vous utilisez une base PostgreSQL locale

---

## Étapes d'installation

### 1. Cloner le repository

```bash
git clone https://github.com/lealjo27/Projet5_new.git
cd Projet5_new
```

### 2. Créer un environnement virtuel

```bash
python -m venv .venv
```

### 3. Activer l'environnement virtuel

#### macOS / Linux

```bash
source .venv/bin/activate
```

#### Windows

```bash
.venv\Scripts\activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. Configurer les variables d'environnement

```bash
cp .env.example .env
```

Modifiez ensuite le fichier `.env` avec vos propres valeurs.

### 6. Démarrer l'application

```bash
uvicorn main:app --reload
```

---

## Accéder à l'API

Une fois l'application démarrée :

```text
Swagger UI : http://localhost:8000/docs
ReDoc      : http://localhost:8000/redoc
```
