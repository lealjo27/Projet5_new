# 🚀 API de Prédiction d'Attrition des Employés

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)
[![Hugging Face](https://img.shields.io/badge/Deploy-Hugging%20Face-yellow.svg)](https://huggingface.co/spaces)
[![NeonDB](https://img.shields.io/badge/Database-NeonDB-green.svg)](https://neon.tech/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Bienvenue dans la documentation du projet **Projet 5 Attrition**.

Cette API REST permet de prédire le risque d'attrition des employés à l'aide d'un modèle de Machine Learning.

Elle est construite avec :

- **FastAPI**
- **PostgreSQL / NeonDB**
- **SQLAlchemy**
- **scikit-learn**
- **Docker**
- **Hugging Face Spaces**

🔗 **API Live** : [Accéder à l'API](https://lealjo27-projet5-attrition-api.hf.space/docs)

---

## Objectif du projet

L'objectif est de fournir une API capable de prédire si un employé présente un risque de départ, à partir de ses données professionnelles et personnelles.

Le modèle de Machine Learning est entraîné avec `scikit-learn`, sérialisé avec `joblib`, puis chargé par l'API pour réaliser des prédictions en temps réel.

---

## Accès rapide

- [Aperçu du projet](apercu.md)
- [Installation locale](installation.md)
- [Configuration](configuration.md)
- [Endpoints API](api.md)
- [Déploiement Hugging Face](deploiement.md)
- [Utilisation](utilisation.md)
