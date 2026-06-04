# Journal de bord individuel

**Nom, prénom :** Rihab [NOM]
**Spécialité :** ESIS ILD — Ingénierie Logiciel & Data Engineering
**Groupe :** Néovolt Grid+

---

| Jour | Ce que j'ai réalisé | Livrable ou trace associé | Difficultés rencontrées |
|------|---------------------|---------------------------|-------------------------|
| Lun 01/06 | Lecture du sujet et du dossier de cas complet. Constitution du groupe. Analyse du besoin Néovolt. Définition de mon périmètre (Volet D). Choix de la stack technique : Python, FastAPI, SQLite, Docker. | Note de cadrage provisoire (commune au groupe) | Compréhension des 5 volets et de leurs interdépendances |
| Mar 02/06 | Mise en place de l'environnement de développement. Lecture du dictionnaire des données. Conception du schéma de la base de données (tables : releves_consommation, clients, compteurs, incidents_reseau, cas_fraude_confirmes, meteo, journaux_securite, actifs_si). Début de l'architecture technique (schéma draw.io). | Schéma d'architecture (brouillon) | Choix entre SQLite (prototype) et PostgreSQL (production) — retenu SQLite pour la rapidité |
| Mer 03/06 | Développement de ingestion.py : chargement des CSV, nettoyage (doublons, valeurs négatives, outliers), stockage SQLite. Développement de main.py (FastAPI) avec 8 endpoints. Tests locaux. Coordination avec le Data Analyst pour récupérer les données nettoyées. | ingestion.py, main.py, neovolt.db | Encodage Windows (cp1252) — résolu avec UTF-8 explicite |
| Jeu 04/06 | Intégration des données nettoyées du Data Analyst. Lancement et tests de tous les endpoints (/releves, /clients, /incidents, /fraudes, /stats/conso, /meteo, /journaux-securite). Création du Dockerfile et docker-compose.yml. Création du repo GitHub. Rédaction du README. | docker-compose.yml, Dockerfile, README.md, commit GitHub | Configuration Docker volume pour neovolt.db |
| Ven 05/06 | Finalisation et tests complets. Enregistrement de la vidéo de démonstration (pipeline + Swagger /docs). Participation à la vidéo de soutenance. Dépôt sur Teams. | Vidéo démo, vidéo soutenance, dossier projet | Coordination pour assembler le dossier PDF final |

---

*Ce journal retrace ma contribution individuelle au projet Néovolt Grid+.*
