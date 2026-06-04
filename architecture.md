# architecture du projet

le principe est simple : on charge les csv avec le script ingestion.py qui fait le nettoyage (doublons, valeurs negatives, outliers) et stocke tout dans une base sqlite. ensuite l'api fastapi lit cette base et expose les donnees.
 
csv -> ingestion.py -> neovolt.db -> api fastapi (port 8000)

j'ai choisi sqlite parce que c'est un prototype et ca evite de configurer un vrai serveur de base de donnees. si on devait passer en prod il faudrait migrer vers postgresql.

pour fastapi j'aime bien la generation automatique de la doc swagger, ca permet aux autres de tester les endpoints sans avoir a tout expliquer.

les tables dans la base : releves_consommation, clients, compteurs, incidents_reseau, cas_fraude_confirmes, meteo, journaux_securite, actifs_si

cote securite les donnees de conso sont des donnees perso donc sensibles rgpd. l'api est en lecture seule. en prod il faudrait ajouter une auth.
