from fastapi import FastAPI, HTTPException
import pandas as pd
import joblib
from pydantic import PositiveInt



app = FastAPI()

# Chargement des datas
try:
    df = pd.read_csv("database/data_preparee.csv")
    df['id'] = df['id'].astype(str)
  
    model = joblib.load("database/modele_attrition.joblib")



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
    
except Exception as e:
    print(f"Erreur chargement du CSV ou du modèle : {e}")


@app.get("/")
def home():
    return {"message" : "API attrition active"}

def read_root():
    return {"message" : "cool ca marche"}

@app.get("/statut")
def check_statut():
    return {"status" : "en attente"}

@app.get("/predict/{id_employe}")
def predict(id_employe: PositiveInt):
    if df is None or model is None:
        raise HTTPException(status_code=500, detail="L'API n'est pas prête (modèle ou data manquants)")
    
    id_str = str(id_employe)

    employe_data = df[df['id'] == id_str]

    if employe_data.empty:
        raise HTTPException(status_code=404, detail=f"L'ID {id_employe} n'existe pas dans la base")

    features = employe_data.drop(columns=['id'], errors='ignore')

    # Prédiction de la probabilité de départ
    try:
        # Probabilité de départ 
        proba_depart = model.predict_proba(features)[0][1]

        prediction = "Risque de départ" if proba_depart >0.5 else "restera probablement"
        
   
        # Calcul des causes (Modèle direct)
        importances = model.feature_importances_
        # Ici, X est déjà "prêt", on utilise .values[0] pour avoir le tableau numpy
        contributions = features.values[0] * importances
        
        top_indices = contributions.argsort()[-3:][::-1]
        top_causes = [FEATURE_NAMES[i].replace('_', ' ').capitalize() for i in top_indices]

        return {
            "employe_id": id_employe,
            "prediction": prediction,
            "probabilite_depart": round(float(proba_depart)*100,2),
            "message": f"Il y a {round(proba_depart *100,1)}% de risques que cet employé parte.",
            "top_3_facteurs_influence": top_causes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction : {e}")

