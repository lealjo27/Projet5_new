# 🏗️ Architecture

## Structure générale

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
│       └── deploy.yml              # CI/CD GitHub Actions
├── database/
│   ├── creation_database.py        # Modèles SQLAlchemy
│   ├── modele_attrition.joblib     # Modèle ML pré-entraîné
│   ├── data_preparee.csv           # Données concernant les salariés
│   └── import_data.py              # Script import des données
├── tests/
│   └── test_main.py                # Tests unitaires
└── README.md                       # Documentation
```

---

## Stack technique

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

## Flux de prédiction

```text
Utilisateur
    |
    | Authentification
    v
API FastAPI
    |
    | Récupération de l'employé
    v
Base PostgreSQL / NeonDB
    |
    | Données employé
    v
Modèle ML scikit-learn
    |
    | Résultat + probabilité
    v
Réponse JSON + sauvegarde en base
```
