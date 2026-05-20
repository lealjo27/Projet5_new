# 🧪 Tests

Les tests unitaires sont réalisés avec `pytest`.

---

## Lancer tous les tests

```bash
python -m pytest tests/ -v -s
```

---

## Lancer un test spécifique

```bash
python -m pytest tests/test_main.py::test_predict_success_with_mock -v -s
```

---

## Lancer les tests avec couverture

```bash
python -m pytest tests/ --cov=.
```

---

## Résultats actuels

```text
✅ 5/6 tests réussis
❌ 1 test edge case en cours de correction
```

---

## Objectifs des tests

Les tests permettent de vérifier :

- le fonctionnement de l'API ;
- l'authentification ;
- les réponses attendues des endpoints ;
- la gestion des erreurs ;
- le comportement de la prédiction avec mock.
