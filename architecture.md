# Architecture - Neovolt Grid+

## Vue d'ensemble

Les donnees brutes (CSV) sont chargees par le pipeline ingestion.py, nettoyees avec pandas, puis stockees dans une base SQLite (neovolt.db). L'API FastAPI lit cette base et expose les donnees via des endpoints REST.

```
CSV (donnees/)
    |
    v
ingestion.py  ->  neovolt.db (SQLite)
                      |
                      v
                  API FastAPI :8000
```

## Pourquoi ces choix

**SQLite** : suffisant pour un prototype, pas besoin de configurer un serveur. En production on passerait sur PostgreSQL.

**FastAPI** : genere automatiquement la doc swagger, pratique pour que les autres membres du groupe puissent tester les endpoints.

**Docker** : pour que n'importe qui puisse relancer le projet sans galetere d'installation.

## Tables dans neovolt.db

- releves_consommation
- clients
- compteurs
- incidents_reseau
- cas_fraude_confirmes
- meteo
- journaux_securite
- actifs_si

## Points RGPD

Les donnees de consommation sont des donnees personnelles. L'API est en lecture seule, sans ecriture possible. En production il faudrait ajouter une authentification (JWT) et du chiffrement.
