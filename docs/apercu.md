# 🎯 Aperçu

Cette API prédit le risque d'attrition, c'est-à-dire le risque de départ d'un employé, à partir de ses données professionnelles et personnelles.

Le modèle de Machine Learning entraîné avec **scikit-learn** est sérialisé avec **joblib** et chargé par l'API pour réaliser des prédictions en temps réel.

---

## 🎓 Cas d'usage

Cette API peut être utilisée par les équipes RH ou data pour :

- 📊 Prédire les employés à risque de départ
- 🎯 Identifier les principaux facteurs influençant l'attrition
- 📈 Surveiller les tendances d'attrition dans l'entreprise
- 🔔 Alerter les équipes RH afin de mettre en place des actions préventives

---

## Principe général

Le fonctionnement global est le suivant :

1. Les données des employés sont stockées en base PostgreSQL.
2. Un utilisateur s'authentifie via un endpoint sécurisé.
3. L'utilisateur appelle l'endpoint de prédiction avec l'identifiant d'un employé.
4. L'API récupère les données de l'employé.
5. Le modèle ML effectue une prédiction.
6. Le résultat est renvoyé sous forme JSON.
7. La prédiction est historisée en base de données.
