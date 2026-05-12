from fastapi import FastAPI
import pandas as pd
app = FastAPI()

# Chargement des datas
try:
    df = pd.read_csv("Database/data_preparee.csv")
    df['id'] = df['id'].astype(str)
except Exception as e:
    print(f"Erreur chargement du CSV : {e}")


@app.get("/")
def read_root():
    return {"message" : "cool ca marche"}

@app.get("/statut")
def check_statut():
    return {"status" : "en attente"}
