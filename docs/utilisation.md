# 💻 Utilisation

Cette page montre comment utiliser l'API après son lancement local ou son déploiement.

---

## Avec Python

```python
import requests

BASE_URL = "https://lealjo27-attrition-api.hf.space"

# 1. Authentification
response = requests.post(
    f"{BASE_URL}/token",
    data={
        "username": "alice",
        "password": "secret123"
    }
)

response.raise_for_status()
token = response.json()["access_token"]

print(f"✅ Token obtenu : {token[:20]}...")

# 2. Faire une prédiction
headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(
    f"{BASE_URL}/predict/20",
    headers=headers
)

response.raise_for_status()
print(response.json())
```

---

## Avec cURL

### 1. S'authentifier

```bash
TOKEN=$(curl -X POST "https://lealjo27-attrition-api.hf.space/token" \
  -d "username=alice&password=secret123" | jq -r '.access_token')

echo "Token : $TOKEN"
```

### 2. Faire une prédiction

```bash
curl -X GET "https://lealjo27-attrition-api.hf.space/predict/20" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Avec Swagger UI

1. Accéder à :

```text
https://lealjo27-attrition-api.hf.space/docs
```

2. Cliquer sur **Authorize**
3. Entrer les identifiants ou le token selon la configuration de sécurité
4. Tester les endpoints directement depuis l'interface
