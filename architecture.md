# Architecture technique — Néovolt Grid+

## Schema

```
+---------------------------+
|   Sources de données      |
|  (CSV Neovolt : relevés,  |
|   clients, météo, etc.)   |
+------------+--------------+
             |
             v
+---------------------------+
|   ingestion.py            |
|   - Chargement CSV        |
|   - Nettoyage pandas      |
|     (doublons, négatifs,  |
|      outliers p99)        |
|   - Stockage SQLite       |
+------------+--------------+
             |
             v
+---------------------------+
|   neovolt.db (SQLite)     |
|   - releves_consommation  |
|   - clients               |
|   - compteurs             |
|   - incidents_reseau      |
|   - cas_fraude_confirmes  |
|   - meteo                 |
|   - journaux_securite     |
|   - actifs_si             |
+------------+--------------+
             |
             v
+---------------------------+
|   API FastAPI (port 8000) |
|   GET /releves            |  --> Dashboards (Data Analyst)
|   GET /clients            |  --> Tous les volets
|   GET /incidents          |  --> Data Analyst, Cybersec
|   GET /fraudes            |  --> Data Scientist, Cybersec
|   GET /stats/conso        |  --> Modèle ML (Data Scientist)
|   GET /meteo              |  --> Modèle ML (Data Scientist)
|   GET /journaux-securite  |  --> Cybersécurité (SIEM)
+------------+--------------+
             |
             v
+---------------------------+
|   Docker Compose          |
|   - service api           |
|   - volume neovolt.db     |
|   - port 8000:8000        |
+---------------------------+

## Choix techniques

| Composant | Choix prototype | Choix production |
|-----------|----------------|-----------------|
| Stockage  | SQLite         | PostgreSQL      |
| API       | FastAPI        | FastAPI + Nginx |
| Pipeline  | pandas         | Apache Spark    |
| Deploy    | Docker Compose | Kubernetes      |

## Sécurité (intégrée à la conception)

- Données personnelles de consommation : sensibles RGPD
- API sans authentification en prototype → JWT tokens en prod
- SCADA réseau : isolé, jamais connecté à cette plateforme
- Logs de sécurité : accessibles uniquement via /journaux-securite (lecture seule)
```
