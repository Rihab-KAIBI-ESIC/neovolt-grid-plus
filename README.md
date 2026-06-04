# neovolt-grid-plus

Plateforme data pour le projet Neovolt - pipeline d'ingestion + API REST

## Comment lancer le projet

### 1. Mettre les CSV dans le dossier donnees/

Les fichiers necessaires : releves_consommation.csv, clients.csv, compteurs.csv, incidents_reseau.csv, cas_fraude_confirmes.csv, meteo.csv, journaux_securite.csv, actifs_si.csv

### 2. Lancer le pipeline

```
pip install -r ingestion/requirements.txt
python ingestion/ingestion.py
```

Ca cree le fichier neovolt.db avec toutes les tables.

### 3. Lancer l'API

```
pip install -r api/requirements.txt
uvicorn api.main:app --reload --port 8000
```

L'API tourne sur http://localhost:8000  
La doc swagger est sur http://localhost:8000/docs

### 4. Avec Docker

```
python ingestion/ingestion.py
docker-compose up --build
```

## Endpoints

- GET / 
- GET /releves
- GET /clients
- GET /incidents
- GET /fraudes
- GET /stats/conso
- GET /meteo
- GET /journaux-securite

Tous les parametres sont visibles dans le swagger /docs
