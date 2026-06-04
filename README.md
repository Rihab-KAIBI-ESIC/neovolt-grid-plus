# Néovolt Grid+ — Plateforme Data

Projet transverse ESIC — Juin 2026
Volet D : Ingénierie Logiciel & Data Engineering

---

## Architecture

```
[CSV nettoyés — dossier donnees/]
          |
          v
[ingestion.py] — pandas → SQLite (neovolt.db)
          |
          v
[FastAPI main.py] — API REST port 8000
          |
          v
[Docker Compose] — conteneurisé
```

---

## Prérequis

- Python 3.11+
- pip
- Docker + Docker Compose (pour le déploiement conteneurisé)

---

## Lancer le projet (sans Docker)

### 1. Copier les données nettoyées dans donnees/

```
donnees/
├── releves_consommation.csv
├── clients.csv
├── compteurs.csv
├── incidents_reseau.csv
├── cas_fraude_confirmes.csv
├── meteo.csv
├── journaux_securite.csv
└── actifs_si.csv
```

### 2. Installer les dépendances et lancer le pipeline

```bash
pip install -r ingestion/requirements.txt
python ingestion/ingestion.py
```

Résultat : fichier `neovolt.db` créé avec toutes les tables.

### 3. Lancer l'API

```bash
pip install -r api/requirements.txt
uvicorn api.main:app --reload --port 8000
```

API disponible sur : http://localhost:8000
Swagger interactif : http://localhost:8000/docs

---

## Lancer avec Docker Compose

```bash
python ingestion/ingestion.py
docker-compose up --build
```

---

## Endpoints disponibles

| Endpoint | Description | Utilisé par |
|----------|-------------|-------------|
| `GET /` | Info API | Tous |
| `GET /releves` | Relevés de consommation | Dashboards |
| `GET /clients` | Référentiel clients | Tous |
| `GET /incidents` | Incidents réseau | Analyse, Cybersécurité |
| `GET /fraudes` | Cas de fraude confirmés | Modèle ML, Cybersécurité |
| `GET /stats/conso` | Stats agrégées par période/zone | Modèle ML |
| `GET /meteo` | Données météo par zone | Modèle ML |
| `GET /journaux-securite` | Logs sécurité | Cybersécurité |

---

## Données sources

Données nettoyées à partir des CSV originaux Néovolt.
Nettoyage appliqué : suppression doublons (1 286), valeurs manquantes (6 856), valeurs négatives (1 034).
Résultat : 503 830 relevés valides, 700 PDL, période 2024-2025.
