# neovolt-grid-plus

projet de fin de semestre - plateforme data pour Neovolt

## lancer le projet

d'abord copier les csv dans le dossier donnees/ puis :

```
pip install -r ingestion/requirements.txt
python ingestion/ingestion.py
```

ensuite pour l'api :

```
pip install -r api/requirements.txt
uvicorn api.main:app --reload --port 8000
```

aller sur http://localhost:8000/docs pour voir tous les endpoints et les tester directement

## avec docker

```
python ingestion/ingestion.py
docker-compose up --build
```

## endpoints dispo

/ , /releves , /clients , /incidents , /fraudes , /stats/conso , /meteo , /journaux-securite

les parametres de filtre sont dans le swagger
