# 🔐 Sécurité

L'API intègre plusieurs mécanismes de sécurité.

---

## Mesures mises en place

- ✅ Authentification par JWT
- ✅ Chiffrement HTTPS via Hugging Face et NeonDB
- ✅ Variables sensibles stockées dans les secrets Hugging Face
- ✅ Validation des entrées côté API
- ✅ Logging des appels pour audit et traçabilité
- ✅ Gestion claire des erreurs HTTP

---

## Authentification JWT

L'utilisateur commence par appeler l'endpoint `/token`.

Si les identifiants sont corrects, l'API retourne un token JWT.

Ce token doit ensuite être transmis dans le header `Authorization` :

```http
Authorization: Bearer {access_token}
```

---

## Recommandation importante

!!! warning "Identifiants par défaut"
    Ne pas conserver d'identifiants par défaut en production.

Remplacez :

```text
alice / secret123
```

par un système utilisateur sécurisé ou une gestion d'accès dédiée.

---

## Bonnes pratiques

- Utiliser une clé `SECRET_KEY` longue et complexe
- Ne jamais versionner le fichier `.env`
- Utiliser les secrets de la plateforme de déploiement
- Renouveler régulièrement les tokens sensibles
- Désactiver ou limiter les comptes de test en production
