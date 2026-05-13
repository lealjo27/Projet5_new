import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

def alimente_table_employes():
    try:
        print("Lecture du csv")
        df = pd.read_csv("./database/data_preparee.csv")

        # mapping a cause rename des colonnes dans la bdd
        mapping = {'id': 'id_employe',
            'statut_marital_Divorcé(e)': 'statut_marital_Divorcé',
            'statut_marital_Marié(e)': 'statut_marital_Marié',
            'departement_Ressources Humaines': 'departement_Ressources_Humaines',
            'poste_Cadre Commercial': 'poste_Cadre_Commercial',
            'poste_Directeur Technique': 'poste_Directeur_Technique',
            'poste_Représentant Commercial': 'poste_Représentant_Commercial',
            'poste_Ressources Humaines': 'poste_Ressources_Humaines',
            'poste_Senior Manager': 'poste_Senior_Manager',
            'poste_Tech Lead': 'poste_Tech_Lead',
            'domaine_etude_Infra & Cloud': 'domaine_etude_Infra_Cloud',
            'domaine_etude_Ressources Humaines': 'domaine_etude_Ressources_Humaines',
            'domaine_etude_Transformation Digitale': 'domaine_etude_Transformation_Digitale'
        }
        df = df.rename(columns=mapping)

        colonnes_valides = [
            'id_employe', 'age', 'genre', 'revenu_mensuel', 'nombre_experiences_precedentes',
            'annee_experience_totale', 'annees_dans_l_entreprise', 'annees_dans_le_poste_actuel',
            'satisfaction_employee_environnement', 'niveau_hierarchique_poste',
            'satisfaction_employee_nature_travail', 'satisfaction_employee_equilibre_pro_perso',
            'heure_supplementaires', 'augmentation_salaire_precedent', 'distance_domicile_travail',
            'annees_depuis_la_derniere_promotion', 'annees_sous_responsable_actuel',
            'statut_marital_Divorcé', 'statut_marital_Marié', 'departement_Consulting',
            'departement_Ressources_Humaines', 'poste_Cadre_Commercial', 'poste_Consultant',
            'poste_Directeur_Technique', 'poste_Manager', 'poste_Représentant_Commercial',
            'poste_Ressources_Humaines', 'poste_Senior_Manager', 'poste_Tech_Lead',
            'domaine_etude_Entrepreunariat', 'domaine_etude_Infra_Cloud', 'domaine_etude_Marketing',
            'domaine_etude_Ressources_Humaines', 'domaine_etude_Transformation_Digitale',
            'Salaire_age', 'duree_par_poste'
        ]
        df_final = df[df.columns.intersection(colonnes_valides)]

        # 4. Insertion
        print(f"🚀 Insertion de {len(df_final)} lignes dans Neon...")
        df_final.to_sql('employes', engine, if_exists='replace', index=False)
        
        print("✅ Importation terminée avec succès !")

    except Exception as e:
        print(f"❌ Erreur lors de l'import : {e}")

if __name__ == "__main__":
    alimente_table_employes()