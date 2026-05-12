from fastapi import FastAPI, HTTPException
import pandas as pd
import joblib



app = FastAPI()

# Chargement des datas
try:
    df = pd.read_csv("database/data_preparee.csv")
    df['id'] = df['id'].astype(str)
  
    model = joblib.load("database/modele_attrition.joblib")
    
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
def predict(id_employe: str):
    if df is None or model is None:
        raise HTTPException(status_code=500, detail="L'API n'est pas prête (modèle ou data manquants)")
    
    employe_data = df[df['id'] == id_employe]

    if employe_data.empty:
        raise HTTPException(status_code=404, detail=f"L'ID {id_employe} n'existe pas dans la base")

    features = employe_data.drop(columns=['id'], errors='ignore')

    # Prédiction de la probabilité de départ
    try:
        proba_depart = model.predict_proba(features)[0][1]

        prediction = "Risque de départ" if proba_depart >0.5 else "restera probablement"

        return {
            "employe_id": id_employe,
            "prediction": prediction,
            "probabilite_depart": round(float(proba_depart)*100,2),
            "message": f"Il y a {round(proba_depart *100,1)}% de risques que cet employé parte."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction : {e}")

