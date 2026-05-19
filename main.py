from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
import pandas as pd
import joblib
from pydantic import PositiveInt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os
from database.creation_database import Employe, Predictions, Logs
from datetime import datetime
import time
from auth import User, get_current_user, Token, fake_users_db, verify_password, create_access_token

app = FastAPI()



  # Obligé d'adapter pour les noms de colonnes 
MAPPING_COLONNES = {
    'age': 'age',
    'genre': 'genre',
    'revenu_mensuel': 'revenu_mensuel',
    'nombre_experiences_precedentes': 'nombre_experiences_precedentes',
    'annee_experience_totale': 'annee_experience_totale',
    'annees_dans_l_entreprise': 'annees_dans_l_entreprise',
    'annees_dans_le_poste_actuel': 'annees_dans_le_poste_actuel',
    'satisfaction_employee_environnement': 'satisfaction_employee_environnement',
    'niveau_hierarchique_poste': 'niveau_hierarchique_poste',
    'satisfaction_employee_nature_travail': 'satisfaction_employee_nature_travail',
    'satisfaction_employee_equilibre_pro_perso': 'satisfaction_employee_equilibre_pro_perso',
    'heure_supplementaires': 'heure_supplementaires',
    'augmentation_salaire_precedent': 'augmentation_salaire_precedent',
    'distance_domicile_travail': 'distance_domicile_travail',
    'annees_depuis_la_derniere_promotion': 'annees_depuis_la_derniere_promotion',
    'annees_sous_responsable_actuel': 'annees_sous_responsable_actuel',
    'statut_marital_Divorcé(e)': 'statut_marital_Divorcé',
    'statut_marital_Marié(e)': 'statut_marital_Marié',
    'departement_Consulting': 'departement_Consulting',
    'departement_Ressources Humaines': 'departement_Ressources_Humaines',
    'poste_Cadre Commercial': 'poste_Cadre_Commercial',
    'poste_Consultant': 'poste_Consultant',
    'poste_Directeur Technique': 'poste_Directeur_Technique',
    'poste_Manager': 'poste_Manager',
    'poste_Représentant Commercial': 'poste_Représentant_Commercial',
    'poste_Ressources Humaines': 'poste_Ressources_Humaines',
    'poste_Senior Manager': 'poste_Senior_Manager',
    'poste_Tech Lead': 'poste_Tech_Lead',
    'domaine_etude_Entrepreunariat': 'domaine_etude_Entrepreunariat',
    'domaine_etude_Infra & Cloud': 'domaine_etude_Infra_Cloud',
    'domaine_etude_Marketing': 'domaine_etude_Marketing',
    'domaine_etude_Ressources Humaines': 'domaine_etude_Ressources_Humaines',
    'domaine_etude_Transformation Digitale': 'domaine_etude_Transformation_Digitale',
    'Salaire_age': 'Salaire_age',
    'duree_par_poste': 'duree_par_poste'
    }
model = None
try:
        model = joblib.load("database/modele_attrition.joblib")
     
except Exception as e:
          print(f"Erreur chargement du modèle : {e}")


FEATURE_NAMES = [
    'age', 'genre', 'revenu_mensuel', 'nombre_experiences_precedentes', 
    'annee_experience_totale', 'annees_dans_l_entreprise', 'annees_dans_le_poste_actuel', 
    'satisfaction_employee_environnement', 'niveau_hierarchique_poste', 
    'satisfaction_employee_nature_travail', 'satisfaction_employee_equilibre_pro_perso', 
    'heure_supplementaires', 'augmentation_salaire_precedent', 'distance_domicile_travail', 
    'annees_depuis_la_derniere_promotion', 'annees_sous_responsable_actuel', 
    'statut_marital_Divorcé(e)', 'statut_marital_Marié(e)', 'departement_Consulting', 
    'departement_Ressources Humaines', 'poste_Cadre Commercial', 'poste_Consultant', 
    'poste_Directeur Technique', 'poste_Manager', 'poste_Représentant Commercial', 
    'poste_Ressources Humaines', 'poste_Senior Manager', 'poste_Tech Lead', 
    'domaine_etude_Entrepreunariat', 'domaine_etude_Infra & Cloud', 'domaine_etude_Marketing', 
    'domaine_etude_Ressources Humaines', 'domaine_etude_Transformation Digitale', 
    'Salaire_age', 'duree_par_poste'
]

# Chargement des datas avec NEON DB

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL","sqlite:///:memory:")

# Connexion à la base / si pas trouvé pour les tests aussi : creer une sqlite en mémoire
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fonction pour ouvrir/fermer la connexion à chaque requête
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message" : "API attrition active"}

def read_root():
    return {"message" : "cool ca marche"}

@app.get("/statut")
def check_statut():
    return {"status" : "en attente"}

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Route permettant d'échanger un username + password contre un jeton JWT.
    """
    # 1. On cherche l'utilisateur dans la base simulée
    user_dict = fake_users_db.get(form_data.username)
    
    # 2. Si l'utilisateur n'existe pas ou que le mot de passe est faux -> Erreur 401
    if not user_dict or not verify_password(form_data.password, user_dict["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiant ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 3. Si l'utilisateur est désactivé
    if user_dict.get("disabled"):
        raise HTTPException(status_code=400, detail="Compte utilisateur désactivé")

    # 4. On prépare les données à enfermer dans le JWT (le "sub" est le standard pour l'identifiant)
    access_token = create_access_token(data={"sub": user_dict["username"]})
    
    # 5. On renvoie le jeton au client
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/predict/{id_employe}")
def predict(id_employe: PositiveInt, 
            db : Session = Depends(get_db), 
            current_user: User = Depends(get_current_user)):
    debut = time.time()
    message_erreur = None
    detail_erreur = None
    id_prediction = None

    employe = db.query(Employe).filter(Employe.id_employe == id_employe).first()
    if not employe:
            raise HTTPException(status_code=404, detail=f"L'ID {id_employe} n'existe pas en base")
    
    # Préparation des données
    donnees_pour_ia = {nom_csv: getattr(employe, nom_bdd) for nom_csv, nom_bdd in MAPPING_COLONNES.items()}
    features = pd.DataFrame([donnees_pour_ia])[FEATURE_NAMES] # Toujours forcer l'ordre des colonnes
 
    try:
        # Calcul prédiction
        proba_depart = model.predict_proba(features)[0][1]
        prediction = "Risque de départ" if proba_depart > 0.5 else "restera probablement"
        
        # Calcul des causes
        importances = model.feature_importances_
        contributions = features.values[0] * importances
        top_indices = contributions.argsort()[-3:][::-1]
        top_causes = [FEATURE_NAMES[i].replace('_', ' ').capitalize() for i in top_indices]
        
        # TRANSFORMATION INDISPENSABLE : liste -> texte pour la BDD
        causes_string = ", ".join(top_causes)

        # Bloc écriture BDD : Predictions
        try:
            new_predict = Predictions(
                id_employe=id_employe,
                prediction=prediction,
                proba=round(float(proba_depart)*100, 2),
                facteurs=causes_string, # On envoie le texte, pas la liste
                date_prediction=datetime.now()
            )
            db.add(new_predict)
            db.commit()
            db.refresh(new_predict)
            id_prediction = new_predict.id
        except Exception as e:
            db.rollback()
            print(f"Erreur BDD : {e}")
            message_erreur = "Erreur lors de l'insertion d'une prédiction"
            detail_erreur = str(e)



        return {
            "employe_id": id_employe,
            "prediction": prediction,
            "probabilite_depart": round(float(proba_depart)*100, 2),
            "message": f"Il y a {round(proba_depart * 100, 1)}% de risques que cet employé parte.",
            "top_3_facteurs_influence": top_causes
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction : {e}")
    
            # Bloc écriture BDD : logs
    finally:
            
        try:
            new_log = Logs(

                id_prediction=id_prediction,
                temps_execution=round(time.time() - debut, 4 ), 
                date_prediction=datetime.now()
            )
            db.add(new_log)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Erreur BDD : {e}")
            message_erreur = "Erreur lors de l'insertion d'un log"
            detail_erreur = str(e)

