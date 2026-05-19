import sys
import os


import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app, get_db
from database.creation_database import Base, Employe

# =========================================================
# 1. CONFIGURATION DE LA BASE DE TEST RESTRUCTURÉE
# =========================================================

# StaticPool force SQLAlchemy à réutiliser l'unique et même connexion en mémoire
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# On surcharge la dépendance de FastAPI
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Client de test unique
client = TestClient(app)

# =========================================================
# 2. FIXTURE DE SESSION SQLITE UNIQUE
# =========================================================

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Force SQLAlchemy à charger les modèles et à créer les tables sur l'engine persistant
    from database.creation_database import Employe, Predictions, Logs
    Base.metadata.create_all(bind=engine)
    
    # Insertion de l'employé virtuel 999
    db = TestingSessionLocal()
    try:
        faux_employe = Employe(
            id_employe=999,
            age=38.0,
            genre=1.0,
            revenu_mensuel=5200.0,
            nombre_experiences_precedentes=3.0,
            annee_experience_totale=12.0,
            annees_dans_l_entreprise=5.0,
            annees_dans_le_poste_actuel=3.0,
            satisfaction_employee_environnement=3.0,
            niveau_hierarchique_poste=2.0,
            satisfaction_employee_nature_travail=4.0,
            satisfaction_employee_equilibre_pro_perso=3.0,
            heure_supplementaires=1.0,
            augmentation_salaire_precedent=14.0,
            distance_domicile_travail=12.0,
            annees_depuis_la_derniere_promotion=1.0,
            annees_sous_responsable_actuel=3.0,
            statut_marital_Divorcé=0.0,
            statut_marital_Marié=1.0,
            departement_Consulting=1.0,
            departement_Ressources_Humaines=0.0,
            poste_Cadre_Commercial=0.0,
            poste_Consultant=1.0,
            poste_Directeur_Technique=0.0,
            poste_Manager=0.0,
            poste_Représentant_Commercial=0.0,
            poste_Ressources_Humaines=0.0,
            poste_Senior_Manager=0.0,
            poste_Tech_Lead=0.0,
            domaine_etude_Entrepreunariat=0.0,
            domaine_etude_Infra_Cloud=1.0,
            domaine_etude_Marketing=0.0,
            domaine_etude_Ressources_Humaines=0.0,
            domaine_etude_Transformation_Digitale=0.0,
            Salaire_age=136.8,
            duree_par_poste=4.0
        )
        db.add(faux_employe)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
    
    yield # Exécution des tests
    
    # Nettoyage
    Base.metadata.drop_all(bind=engine)


# =========================================================
# 3. TOUS LES TESTS UNITAIRES
# =========================================================

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200 

def test_placeholder():
    assert 1 + 1 == 2

def test_predict_sans_token():
    response = client.get("/predict/999")
    assert response.status_code in [401, 403]

def test_login_succes():
    response = client.post(
        "/token",
        data={"username": "alice", "password": "secret123"}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "access_token" in json_data
    assert json_data["token_type"] == "bearer"

def test_login_wrong_password():
    response = client.post(
        "/token",
        data={"username": "alice", "password": "mauvais_password"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Identifiant ou mot de passe incorrect"

def test_predict_success():
    """Vérifie le succès de la prédiction avec authentification."""
    # Authentification pour récupérer le jeton d'accès
    login_response = client.post(
        "/token",
        data={"username": "alice", "password": "secret123"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Appel de l'API pour l'employé virtuel qui partage désormais la même mémoire
    response = client.get("/predict/999", headers=headers)
    
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["employe_id"] == 999
    assert "prediction" in json_data
    assert "probabilite_depart" in json_data