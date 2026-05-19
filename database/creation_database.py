import os
from sqlalchemy import create_engine, text, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

# Connexion à la BDD

load_dotenv(os.path.join(os.getcwd(), '.env'))
url = os.getenv("DATABASE_URL")

try:
    engine = create_engine(url)

    with engine.connect() as conn:
        result = conn.execute(text("SELECT 'Connexion Réussie'"))
        print(result.all()[0][0])
except Exception as e:
    print(f"Erreur de connexion : {e}")

#Création de la BDD
Base = declarative_base()

# Création des tables

class Employe(Base):
    __tablename__ = "employes"
    id_employe = Column(Integer, primary_key=True, autoincrement=False)
    age = Column(Float)
    genre = Column(Float)
    revenu_mensuel = Column(Float)
    nombre_experiences_precedentes = Column(Float)
    annee_experience_totale = Column(Float)
    annees_dans_l_entreprise = Column(Float)
    annees_dans_le_poste_actuel = Column(Float)
    satisfaction_employee_environnement = Column(Float)
    niveau_hierarchique_poste = Column(Float)
    satisfaction_employee_nature_travail = Column(Float)
    satisfaction_employee_equilibre_pro_perso = Column(Float)
    heure_supplementaires = Column(Float)
    augmentation_salaire_precedent = Column(Float)
    distance_domicile_travail = Column(Float)
    annees_depuis_la_derniere_promotion = Column(Float)
    annees_sous_responsable_actuel = Column(Float)
    statut_marital_Divorcé = Column(Float)
    statut_marital_Marié = Column(Float)
    departement_Consulting = Column(Float)
    departement_Ressources_Humaines = Column(Float)
    poste_Cadre_Commercial = Column(Float)
    poste_Consultant = Column(Float)
    poste_Directeur_Technique = Column(Float)
    poste_Manager = Column(Float)
    poste_Représentant_Commercial = Column(Float)
    poste_Ressources_Humaines = Column(Float)
    poste_Senior_Manager = Column(Float)
    poste_Tech_Lead = Column(Float)
    domaine_etude_Entrepreunariat = Column(Float)
    domaine_etude_Infra_Cloud = Column(Float)
    domaine_etude_Marketing = Column(Float)
    domaine_etude_Ressources_Humaines = Column(Float)
    domaine_etude_Transformation_Digitale = Column(Float)
    Salaire_age = Column(Float)
    duree_par_poste = Column(Float)

class Predictions(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_employe = Column(Integer)
    prediction = Column(String(50))
    proba = Column(Float)
    facteurs = Column(String)
    date_prediction = Column(DateTime)

class Logs(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_prediction = Column(Integer)
    temps_execution = Column(Float)
    date_prediction = Column(DateTime)
    erreur = Column(String(50))
    detail_erreur = Column(String)


def init_db():
    try:
        print("Création des tables sur Neon")
        Base.metadata.create_all(bind=engine)
        print("Création des tables ok ")
    except Exception as e:
        print(f" Erreur création des tables : {e}")

if __name__ == "__main__":
    init_db()