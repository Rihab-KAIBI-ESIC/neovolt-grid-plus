# Neovolt Grid+

Plateforme data pour le projet Neovolt — Volet D : Ingénierie Logiciel & Data Engineering.

L'idée c'est de centraliser toutes les données (relevés de compteurs, clients, météo, incidents, journaux de sécurité) dans une base SQLite et de les exposer via une API REST pour que les autres volets puissent travailler dessus.

---

## Ce qu'il y a dans le projet

```
neovolt-grid-plus/
├── ingestion/
│   ├── ingestion.py       script de chargement CSV → SQLite
│   └── requirements.txt
├── api/
│   ├── main.py            API FastAPI, 8 endpoints
│   ├── requirements.txt
│   └── Dockerfile
├── donnees/               mettre les CSV ici avant de lancer l'ingestion
├── docker-compose.yml
├── architecture.md        choix techniques et schéma
├── neovolt.db             base générée par ingestion.py (pas dans le repo)
└── README.md
```

---

## Prérequis

- Python 3.7 ou plus
- pip
- les fichiers CSV dans le dossier `donnees/` (fournis par le Data Analyst)
- Docker si on veut lancer avec docker-compose

---

## Lancer le projet

### Étape 1 — charger les données

A faire une seule fois. Ca crée le fichier `neovolt.db`.

```bash
pip install -r ingestion/requirements.txt
python ingestion/ingestion.py
```

Le script affiche l'avancement et le nombre de lignes chargées par table. Ca prend environ 30 secondes.

### Étape 2 — lancer l'API

```bash
pip install -r api/requirements.txt
python -m uvicorn api.main:app --reload --port 8000
```

L'API est disponible sur http://localhost:8000  
La doc Swagger est sur http://localhost:8000/docs — c'est là qu'on peut tester tous les endpoints directement.

### Avec Docker

```bash
python ingestion/ingestion.py   # d'abord créer la base
docker-compose up --build
```

---

## Les endpoints disponibles

| endpoint | paramètres principaux | pour qui |
|---|---|---|
| GET / | — | vérification que l'API tourne |
| GET /releves | zone, date_debut, date_fin, limit | Data Analyst |
| GET /clients | segment, limit | tous |
| GET /incidents | zone, type_incident, limit | Data Analyst, Cybersécurité |
| GET /fraudes | type_fraude | Data Scientist, Cybersécurité |
| GET /stats/conso | zone, granularite (jour/semaine/mois) | Data Scientist |
| GET /meteo | zone, date_debut, date_fin, limit | Data Scientist |
| GET /journaux-securite | systeme, type_evenement, limit | Cybersécurité |

Tous les filtres sont optionnels. Le Swagger sur `/docs` permet de les tester interactivement.

---

## Valeurs utiles pour tester

- zones : `Centre-Ville`, `Zone-Industrielle`, `Val-Nord`, `Parc-Tertiaire`, `Rives-Sud`, `Bourg-Ancien`, `Coteaux-Ouest`, `Plateau-Est`
- segments clients : `particulier`, `petit_pro`, `collectivite`, `entreprise`
- types incidents : `coupure`, `surtension`, `panne_poste`, `baisse_tension`, `maintenance_programmee`
- types fraude : `sous_comptage`, `compteur_trafique`, `branchement_illicite`
- systèmes journaux : `scada`, `active_directory`, `vpn`, `plateforme_data`, `portail_client`
- plage de dates : 2024-01-01 → 2025-12-12
