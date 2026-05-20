# 📡 API Endpoints

Cette page décrit les principaux endpoints exposés par l'API.

---

## 🔓 Racine

```http
GET /
```

### Description

Permet de vérifier que l'API est active.

### Réponse

```json
{
  "message": "API attrition active"
}
```

---

## 🔐 Authentification

```http
POST /token
Content-Type: application/x-www-form-urlencoded
```

### Description

Permet d'obtenir un token JWT utilisé pour accéder aux endpoints protégés.

### Corps de requête

```text
username=alice&password=secret123
```

### Réponse

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Utilisateur par défaut

```text
alice / secret123
```

---

## 🎯 Prédiction

```http
GET /predict/{id_employe}
Authorization: Bearer {access_token}
```

### Description

Endpoint protégé nécessitant un token JWT.

Il permet de prédire le risque de départ d'un employé à partir de son identifiant.

### Paramètre de chemin

| Paramètre | Type | Description |
|---|---|---|
| `id_employe` | integer | Identifiant de l'employé |

### Exemple avec cURL

```bash
curl -X GET "http://localhost:8000/predict/20" \
  -H "Authorization: Bearer votre_token_jwt"
```

### Réponse réussie `200`

```json
{
  "employe_id": 20,
  "prediction": "Risque de départ",
  "probabilite_depart": 85.0,
  "message": "Il y a 85.0% de risques que cet employé parte.",
  "top_3_facteurs_influence": [
    "Distance domicile travail",
    "Heure supplementaires",
    "Satisfaction employee equilibre pro perso"
  ]
}
```

### Réponse erreur `404`

```json
{
  "detail": "L'ID 999 n'existe pas en base"
}
```
