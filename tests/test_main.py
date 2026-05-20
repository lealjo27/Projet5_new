import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import MagicMock, patch
from database.creation_database import Employe
import numpy as np

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

def test_predict_success_with_mock():
    """Test fonctionnel complet avec Mock BDD ET Mock du modèle ML."""
    
    # 1. Création du faux employé
    faux_employe = Employe(
        id_employe=20, age=38.0, genre=1.0, revenu_mensuel=5200.0,
        nombre_experiences_precedentes=3.0, annee_experience_totale=12.0,
        annees_dans_l_entreprise=5.0, annees_dans_le_poste_actuel=3.0,
        satisfaction_employee_environnement=3.0, niveau_hierarchique_poste=2.0,
        satisfaction_employee_nature_travail=4.0, satisfaction_employee_equilibre_pro_perso=3.0,
        heure_supplementaires=1.0, augmentation_salaire_precedent=14.0,
        distance_domicile_travail=12.0, annees_depuis_la_derniere_promotion=1.0,
        annees_sous_responsable_actuel=3.0, statut_marital_Divorcé=0.0,
        statut_marital_Marié=1.0, departement_Consulting=1.0,
        departement_Ressources_Humaines=0.0, poste_Cadre_Commercial=0.0,
        poste_Consultant=1.0, poste_Directeur_Technique=0.0, poste_Manager=0.0,
        poste_Représentant_Commercial=0.0, poste_Ressources_Humaines=0.0,
        poste_Senior_Manager=0.0, poste_Tech_Lead=0.0, domaine_etude_Entrepreunariat=0.0,
        domaine_etude_Infra_Cloud=1.0, domaine_etude_Marketing=0.0,
        domaine_etude_Ressources_Humaines=0.0, domaine_etude_Transformation_Digitale=0.0,
        Salaire_age=136.8, duree_par_poste=4.0
    )

    # 2. Mock de la base de données
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = faux_employe

    from main import get_db
    app.dependency_overrides[get_db] = lambda: mock_db

    # 3. 🛠️ MOCK DU MODÈLE DE MACHINE LEARNING
    mock_model = MagicMock()
    mock_model.predict_proba.return_value = np.array([[0.15, 0.85]])
    mock_model.feature_importances_ = np.ones(35) / 35  # 35 features (pas 34!)

    with patch('main.model', mock_model):
        # 4. Authentification
        login_response = client.post("/token", data={"username": "alice", "password": "secret123"})
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 5. Appel de la route
        response = client.get("/predict/20", headers=headers)

    # 6. Nettoyage
    app.dependency_overrides.pop(get_db, None)

    # 7. Assertions
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["employe_id"] == 20
    assert "prediction" in json_data
    assert "probabilite_depart" in json_data
    assert json_data["prediction"] == "Risque de départ"
    assert json_data["probabilite_depart"] == 85.0


def test_predict_edge_case_high_risk():
    """Test fonctionnel : employé avec profil à très haut risque de départ."""

    # 1. Création d'un employé critique
    employe_critique = Employe(
        id_employe=888, age=19.0, genre=0.0, revenu_mensuel=1200.0,
        nombre_experiences_precedentes=1.0, annee_experience_totale=1.0,
        annees_dans_l_entreprise=1.0, annees_dans_le_poste_actuel=1.0,
        satisfaction_employee_environnement=1.0, niveau_hierarchique_poste=1.0,
        satisfaction_employee_nature_travail=1.0, satisfaction_employee_equilibre_pro_perso=1.0,
        heure_supplementaires=1.0, augmentation_salaire_precedent=10.0,
        distance_domicile_travail=45.0, annees_depuis_la_derniere_promotion=0.0,
        annees_sous_responsable_actuel=1.0, statut_marital_Divorcé=0.0,
        statut_marital_Marié=0.0, departement_Consulting=1.0,
        departement_Ressources_Humaines=0.0, poste_Consultant=1.0, 
        poste_Cadre_Commercial=0.0, poste_Directeur_Technique=0.0, poste_Manager=0.0,
        poste_Représentant_Commercial=0.0, poste_Ressources_Humaines=0.0,
        poste_Senior_Manager=0.0, poste_Tech_Lead=0.0, domaine_etude_Entrepreunariat=0.0,
        domaine_etude_Infra_Cloud=1.0, domaine_etude_Marketing=0.0,
        domaine_etude_Ressources_Humaines=0.0, domaine_etude_Transformation_Digitale=0.0,
        Salaire_age=63.1, duree_par_poste=1.0
    )
    
    # 2. Mock de la base de données
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = employe_critique
    
    from main import get_db
    app.dependency_overrides[get_db] = lambda: mock_db
    
    # 3. Mock du modèle avec très haute probabilité de départ
    mock_model = MagicMock()
    mock_model.predict_proba.return_value = np.array([[0.2, 0.8]])
    mock_model.feature_importances_ = np.ones(35) / 35  # 35 features (pas 34!)

    with patch('main.model', mock_model):
        # 4. Authentification
        login_response = client.post("/token", data={"username": "alice", "password": "secret123"})
        headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
        
        # 5. Appel de la route
        response = client.get("/predict/888", headers=headers)

    # 6. Nettoyage
    app.dependency_overrides.pop(get_db, None)
    
    # 7. Assertions
    assert response.status_code == 200
    assert response.json()["prediction"] == "Risque de départ"
    assert response.json()["probabilite_depart"] == 80.0

from main import get_db

def test_predict_employe_not_found():
    """Vérifie que l'API renvoie bien une 404 si l'ID est inconnu."""
    # Mock de BDD qui renvoie 'None' (l'employé n'existe pas)
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None 
    
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    # Auth
    login_response = client.post("/token", data={"username": "alice", "password": "secret123"})
    headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
    
    # Appel
    response = client.get("/predict/9999", headers=headers)
    
    app.dependency_overrides.pop(get_db, None)
    
    # Assertion
    assert response.status_code == 404
    assert response.json()["detail"] == "L'ID 9999 n'existe pas en base"

def test_predict_db_exception():
    """Test que l'API lève bien une exception quand la BDD est en panne."""
    
    # 1. Mock de la base de données
    mock_db = MagicMock()
    # On simule l'exception technique
    mock_db.query.side_effect = Exception("Erreur BDD technique")
    
    # 2. Injection du mock
    app.dependency_overrides[get_db] = lambda: mock_db
    
    # 3. Authentification
    login_response = client.post("/token", data={"username": "alice", "password": "secret123"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 4. ASSERTION : On attend explicitement l'exception
    # Le test passe si l'exception est levée. 
    # S'il n'y a pas d'exception, le test échoue (c'est ce qu'on veut !)
    with pytest.raises(Exception, match="Erreur BDD technique"):
        client.get("/predict/20", headers=headers)
        
    # 5. Nettoyage
    app.dependency_overrides.pop(get_db, None)

def test_predict_invalid_token():
#Test l'accès avec un token corrompu.
    headers = {"Authorization": "Bearer token_bidon_invalide"}
    response = client.get("/predict/20", headers=headers)
    
    # Normalement, doit renvoyer 401 ou 403
    assert response.status_code in [401, 403]
