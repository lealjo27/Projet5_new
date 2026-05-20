# 🚀 Déploiement Hugging Face

L'API peut être déployée sur **Hugging Face Spaces** avec le SDK Docker.

---

## Prérequis

- Un compte Hugging Face : [https://huggingface.co/](https://huggingface.co/)
- Un token d'accès Hugging Face : `Settings → Access Tokens`

---

## 1. Créer un Space Hugging Face

Sur [https://huggingface.co/spaces](https://huggingface.co/spaces), créer un nouveau Space :

```text
Nom       : attrition-api
Owner     : votre username
License   : MIT
Visibility: Public ou Private
SDK       : Docker
```

---

## 2. Cloner le Space

```bash
git clone https://huggingface.co/spaces/lealjo27/attrition-api
cd attrition-api
```

---

## 3. Ajouter les fichiers du projet

```bash
cp ../Projet5_new/main.py .
cp ../Projet5_new/auth.py .
cp ../Projet5_new/requirements.txt .
cp ../Projet5_new/Dockerfile .
cp -r ../Projet5_new/database/ .
```

---

## 4. Configurer les secrets

Dans le Space Hugging Face :

```text
Settings → Repository secrets
```

Ajouter :

```text
DATABASE_URL = postgresql://user:password@ep-xxxx...
SECRET_KEY = votre-cle-secrete
```

---

## 5. Pousser le code

```bash
git add .
git commit -m "Déploiement initial API attrition"
git push origin main
```

---

## 6. Accéder à l'API

Après le build, l'API sera disponible à l'adresse :

```text
https://lealjo27-attrition-api.hf.space
```

Endpoints utiles :

```text
Swagger UI : https://lealjo27-attrition-api.hf.space/docs
API        : https://lealjo27-attrition-api.hf.space/predict/20
```
