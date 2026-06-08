# Architecture — Neovolt Grid+

## Comment ca marche globalement

J'ai construit la plateforme autour de trois briques : un script d'ingestion qui charge les données, une base SQLite qui centralise tout, et une API FastAPI qui expose les données aux autres volets. 


donnees CSV (relevés, clients, météo, incidents, etc.)
              |
              v
       [ ingestion.py ]
       nettoyage pandas
       (doublons, valeurs
        négatives, outliers)
              |
              v
       [ neovolt.db ]
         SQLite local
              |
              v
       [ API FastAPI ]
         port 8000
         lecture seule
              |
    __________|__________
    |         |          |
    v         v          v
 Volet B   Volet C    Volet E
 Analyst   Scientist  Cybersec




## Le pipeline d'ingestion

J'ai fait le choix de partir sur du **batch** avec pandas plutôt que du temps réel. La raison c'est simple : les données arrivent sous forme de CSV, pas depuis des compteurs en direct. Donc pas besoin de Kafka pour le prototype.

Concrètement `ingestion.py` fait ça dans l'ordre :
- charge les CSV un par un depuis le dossier `donnees/`
- sur les relevés de conso : supprime les doublons, retire les consommations négatives, et coupe les outliers au-dessus du 99e percentile
- charge tout dans SQLite avec `to_sql`

Ca prend environ 30 secondes pour 434 955 relevés, ce qui est tout à fait acceptable pour un prototype.

**Ce que j'aurais mis en production :** si on avait les compteurs qui envoient des relevés toutes les 30 min en temps réel, là il faudrait Kafka pour absorber le flux (600 000 compteurs × 2 relevés/h = 1,2 million de messages par heure). Derrière Kafka on mettrait Spark Streaming pour le traitement, et Airflow pour orchestrer les jobs de nettoyage. Pour l'instant pandas fait le job.

---

## La base de données

J'ai choisi SQLite parce que c'est un prototype. Pas de serveur à configurer, tout est dans un seul fichier `neovolt.db`, et pour 500 000 lignes en lecture ça tourne sans problème.

Les tables :

| table | lignes | contenu |
|---|---|---|
| releves_consommation | 434 955 | relevés 30 min par compteur |
| clients | 700 | référentiel clients |
| compteurs | 700 | référentiel compteurs |
| meteo | 5 848 | données météo par zone |
| incidents_reseau | 420 | pannes et incidents |
| cas_fraude_confirmes | 24 | fraudes détectées |
| journaux_securite | 47 824 | logs de sécurité |
| actifs_si | 28 | inventaire du SI |

**Limites de SQLite que je suis conscient de :** pas de connexions en écriture concurrentes, pas de haute dispo, pas de gestion fine des droits. En production il faudrait passer sur PostgreSQL avec une réplication pour la HA, et partitionner la table de relevés par zone et par mois parce qu'elle va grossir vite.

---

## L'API

8 endpoints en lecture seule. J'ai fait le choix du read-only volontairement : l'API ne doit pas modifier des données sur une infrastructure critique, et ca simplifie aussi la sécurité.

J'ai utilisé FastAPI parce que la doc Swagger est générée automatiquement, ce qui permettait aux autres volets de tester sans que j'aie à tout leur expliquer. Et les performances async de FastAPI sont bien meilleures qu'un framework synchrone si on montait en charge.

Ce que chaque volet utilise :

- **Volet B (Data Analyst)** → `/releves` pour alimenter les dashboards, `/incidents` pour la cartographie réseau
- **Volet C (Data Scientist)** → `/stats/conso` pour les séries temporelles, `/meteo` pour les corrélations, `/fraudes` pour entraîner le modèle de détection
- **Volet E (Cybersécurité)** → `/journaux-securite` pour le SIEM, `/fraudes` pour l'audit


---

## Déploiement

J'ai conteneurisé l'API avec Docker. Le `Dockerfile` part d'une image python:3.11-slim, installe les dépendances et lance uvicorn. Le `docker-compose.yml` monte la base en volume pour que les données survivent aux redémarrages.

Pour une mise en production réelle, le pas suivant ce serait de déployer sur un cloud (Azure ou AWS) avec Kubernetes pour gérer la scalabilité horizontale. On pourrait aussi ajouter un cache Redis devant les endpoints de stats puisque les requêtes GROUP BY sur 400k lignes sont coûteuses et les résultats changent pas toutes les secondes.
