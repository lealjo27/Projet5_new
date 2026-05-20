# 📚 Structure du projet

Cette page décrit les principaux fichiers du projet.

---

## Fichiers principaux

| Fichier | Rôle |
|---|---|
| `main.py` | Application FastAPI principale |
| `auth.py` | Gestion de l'authentification JWT |
| `database/creation_database.py` | Modèles SQLAlchemy |
| `database/modele_attrition.joblib` | Modèle ML sérialisé |
| `database/data_preparee.csv` | Données préparées des salariés |
| `database/import_data.py` | Script d'import des données |
| `requirements.txt` | Dépendances Python |
| `Dockerfile` | Image Docker de l'application |
| `docker-compose.yml` | Orchestration locale API + base de données |
| `tests/test_main.py` | Suite de tests unitaires |
| `.env.example` | Template de configuration |
| `.github/workflows/tests.yml` | Pipeline CI/CD GitHub Actions |

---

## Organisation recommandée

```text
Projet5_new/
├── main.py
├── auth.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── database/
├── tests/
├── docs/
├── mkdocs.yml
└── README.md
```
