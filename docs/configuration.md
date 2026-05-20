# ⚙️ Configuration

La configuration de l'application se fait via un fichier `.env` placé à la racine du projet.

---

## Exemple de fichier `.env`

```env
# Base de données NeonDB
DATABASE_URL=postgresql://user:password@ep-xxxx.eu-west-1.aws.neon.tech/dbname?sslmode=require

# Sécurité JWT
SECRET_KEY=votre-cle-secrete-tres-longue-et-complexe
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Variables d'environnement

| Variable | Description |
|---|---|
| `DATABASE_URL` | URL de connexion à la base PostgreSQL ou NeonDB |
| `SECRET_KEY` | Clé secrète utilisée pour signer les tokens JWT |
| `ALGORITHM` | Algorithme de signature JWT, par exemple `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Durée de validité du token d'accès |

---

## Obtenir une `DATABASE_URL` NeonDB

1. Créer un compte sur [https://neon.tech/](https://neon.tech/)
2. Créer un projet PostgreSQL
3. Copier la connection string
4. Ajouter le paramètre SSL si nécessaire

Exemple :

```env
DATABASE_URL=postgresql://user:password@ep-xxxx.eu-west-1.aws.neon.tech/mydb?sslmode=require
```

---

## Recommandations

!!! warning "Sécurité"
    Ne committez jamais votre fichier `.env` dans Git.

Ajoutez-le dans le fichier `.gitignore` :

```gitignore
.env
```
