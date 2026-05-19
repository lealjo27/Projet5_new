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

from unittest.mock import MagicMock
from database.creation_database import Employe

def test_predict_success_with_mock():
    """Test fonctionnel de la route de prédiction en simulant (mockant) la BDD."""
    
    # 1. On crée un faux employé en mémoire 
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

    # 2. On mock la session de base de données
    mock_db = MagicMock()
    # On simule l'enchaînement : db.query().filter().first() -> renvoie notre faux_employe
    mock_db.query.return_value.filter.return_value.first.return_value = faux_employe

    # 3. On court-circuite temporairement la dépendance get_db de FastAPI
    from main import get_db
    app.dependency_overrides[get_db] = lambda: mock_db

    # 4. On s'authentifie pour avoir le token nécessaire
    login_response = client.post("/token", data={"username": "alice", "password": "secret123"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 5. Appel de la route (elle passera à travers TOUT ton code de prédiction ML dans main.py)
    response = client.get("/predict/20", headers=headers)

    # 6. Nettoyage de la surcharge
    app.dependency_overrides.pop(get_db, None)

    # 7. Assertions
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["employe_id"] == 20
    assert "prediction" in json_data
    assert "probabilite_depart" in json_data


    def test_predict_edge_case_high_risk():
    #Test fonctionnel : employé avec profil à très haut risque de départ.

        mock_db = MagicMock()
        # Profil extrême : Jeune, bas salaire, bcp d'heures supp, insatisfait
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
        mock_db.query.return_value.filter.return_value.first.return_value = employe_critique
        
        from main import get_db
        app.dependency_overrides[get_db] = lambda: mock_db
        
        # Auth
        login_response = client.post("/token", data={"username": "alice", "password": "secret123"})
        headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
        
        response = client.get("/predict/888", headers=headers)
        app.dependency_overrides.pop(get_db, None)
        
        assert response.status_code == 200
        assert response.json()["prediction"] == "Risque de départ"
        assert response.json()["probabilite_depart"] > 70.0  # On attend une forte probabilité