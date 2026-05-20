# 🐳 Docker

Le projet peut être lancé dans un conteneur Docker.

---

## Lancer localement avec Docker

### Construire l'image

```bash
docker build -t attrition-api .
```

### Lancer le conteneur

```bash
docker run -p 8000:8000 --env-file .env attrition-api
```

L'API sera disponible sur :

```text
http://localhost:8000/docs
```

---

## Lancer avec Docker Compose

### Démarrer les services

```bash
docker-compose up -d
```

### Arrêter les services

```bash
docker-compose down
```

### Voir les logs

```bash
docker-compose logs -f api
```

---

## Exemple de `docker-compose.yml`

```yaml
version: "3.8"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: attrition_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```
