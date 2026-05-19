import sys
import os
# Assure que Python trouve main.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from main import app

# Initialisation du client de test standard
client = TestClient(app)

# =========================================================
# TESTS UNITAIRES DE L'API
# =========================================================

def test_read_root():
    """Vérifie que la racine de l'API répond correctement."""
    response = client.get("/")
    assert response.status_code == 200 

def test_placeholder():
    """Test de base pour s'assurer que pytest tourne."""
    assert 1 + 1 == 2

def test_predict_sans_token():
    """Vérifie que la route /predict bloque l'accès sans authentification."""
    response = client.get("/predict/42")
    assert response.status_code in [401, 403]

def test_login_succes():
    """Vérifie qu'un utilisateur valide reçoit bien un token JWT."""
    response = client.post(
        "/token",
        data={"username": "alice", "password": "secret123"}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "access_token" in json_data
    assert json_data["token_type"] == "bearer"

def test_login_wrong_password():
    """Vérifie qu'un mauvais mot de passe est bien rejeté."""
    response = client.post(
        "/token",
        data={"username": "alice", "password": "mauvais_password"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Identifiant ou mot de passe incorrect"