# 📊 Base de données

Le projet utilise une base de données PostgreSQL, hébergée localement ou via NeonDB.

---

## Table `employe`

Contient les données des employés utilisées pour effectuer les prédictions.

```sql
SELECT *
FROM employe
LIMIT 5;
```

---

## Table `predictions`

Contient l'historique des prédictions effectuées par l'API.

```sql
SELECT employe_id, prediction, proba, facteurs, date_prediction
FROM predictions
ORDER BY date_prediction DESC
LIMIT 10;
```

---

## Table `logs`

Contient les logs d'exécution des appels API.

```sql
SELECT id_prediction, temps_execution, date_prediction
FROM logs
ORDER BY date_prediction DESC
LIMIT 10;
```

---

## Rôle de la base de données

La base de données permet de :

- stocker les employés ;
- récupérer les informations nécessaires à la prédiction ;
- historiser les résultats ;
- conserver des logs d'exécution ;
- auditer les appels réalisés à l'API.
