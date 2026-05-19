---
title: Projet 5 Attrition
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
python_version: "3.12"
---
# Projet 5 : API de Prédiction d'Attrition

Ce projet contient une API construite avec **FastAPI** permettant de prédire la probabilité de départ d'un employé.

## 🚀 Installation
1. Créer un environnement virtuel : `python -m venv .venv`
2. Installer les dépendances : `pip install fastapi uvicorn pandas`

## 🛠 Utilisation
Lancer l'API :
```bash
uvicorn main:app --reload