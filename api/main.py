"""
API REST — Néovolt Grid+
"""

from fastapi import FastAPI, Query, HTTPException
import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "neovolt.db")

app = FastAPI(
    title="Néovolt Grid+ API",
    description="API de la plateforme data Néovolt — projet ESIC 2026",
    version="1.0.0",
)


def get_db():
    if not os.path.exists(DB_PATH):
        raise HTTPException(
            status_code=503,
            detail="Base de données non disponible. Lancez d'abord ingestion.py."
        )
    return sqlite3.connect(DB_PATH)


@app.get("/", tags=["Info"])
def root():
    return {
        "projet": "Néovolt Grid+",
        "version": "1.0.0",
        "endpoints": ["/releves", "/clients", "/incidents", "/fraudes", "/stats/conso", "/docs"],
    }


@app.get("/releves", tags=["Consommation"])
def get_releves(
    zone: str = Query(None, description="Filtrer par zone (ex: Centre-Ville)"),
    date_debut: str = Query(None, description="Date début (YYYY-MM-DD)"),
    date_fin: str = Query(None, description="Date fin (YYYY-MM-DD)"),
    limit: int = Query(1000, le=10000, description="Nombre max de lignes"),
):
    """Relevés de consommation — pour les dashboards Data Analyst."""
    conn = get_db()
    query = "SELECT * FROM releves_consommation WHERE 1=1"
    params = []
    if zone:
        query += " AND zone = ?"
        params.append(zone)
    if date_debut:
        query += " AND date >= ?"
        params.append(date_debut)
    if date_fin:
        query += " AND date <= ?"
        params.append(date_fin)
    query += f" LIMIT {limit}"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df.to_dict(orient="records")


@app.get("/clients", tags=["Référentiels"])
def get_clients(
    segment: str = Query(None, description="particulier | petit_pro | entreprise | collectivite"),
    limit: int = Query(500, le=5000),
):
    """Référentiel clients — pour tous les volets."""
    conn = get_db()
    query = "SELECT * FROM clients WHERE 1=1"
    params = []
    if segment:
        query += " AND segment = ?"
        params.append(segment)
    query += f" LIMIT {limit}"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df.to_dict(orient="records")


@app.get("/incidents", tags=["Réseau"])
def get_incidents(
    zone: str = Query(None, description="Zone géographique"),
    type_incident: str = Query(None, description="coupure | surtension | panne_poste | ..."),
    limit: int = Query(500, le=5000),
):
    """Incidents réseau — pour Cybersécurité et Data Analyst."""
    conn = get_db()
    query = "SELECT * FROM incidents_reseau WHERE 1=1"
    params = []
    if zone:
        query += " AND zone = ?"
        params.append(zone)
    if type_incident:
        query += " AND type = ?"
        params.append(type_incident)
    query += f" LIMIT {limit}"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df.to_dict(orient="records")


@app.get("/fraudes", tags=["Sécurité"])
def get_fraudes(
    type_fraude: str = Query(None, description="sous_comptage | branchement_illicite | compteur_trafique"),
):
    """Cas de fraude confirmés — pour Data Scientist (modèle ML) et Cybersécurité."""
    conn = get_db()
    query = "SELECT * FROM cas_fraude_confirmes WHERE 1=1"
    params = []
    if type_fraude:
        query += " AND type_fraude = ?"
        params.append(type_fraude)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df.to_dict(orient="records")


@app.get("/stats/conso", tags=["Data Science"])
def get_stats_conso(
    zone: str = Query(None, description="Filtrer par zone"),
    granularite: str = Query("jour", description="jour | semaine | mois"),
):
    """
    Statistiques agrégées de consommation — pour le modèle ML du Data Scientist.
    Retourne moyenne, min, max, total par période et zone.
    """
    conn = get_db()
    if granularite == "mois":
        date_trunc = "strftime('%Y-%m', date)"
    elif granularite == "semaine":
        date_trunc = "strftime('%Y-%W', date)"
    else:
        date_trunc = "date"

    query = f"""
        SELECT
            {date_trunc} as periode,
            zone,
            COUNT(*) as nb_releves,
            ROUND(AVG(consommation_kwh), 2) as conso_moyenne_kwh,
            ROUND(MIN(consommation_kwh), 2) as conso_min_kwh,
            ROUND(MAX(consommation_kwh), 2) as conso_max_kwh,
            ROUND(SUM(consommation_kwh), 2) as conso_totale_kwh
        FROM releves_consommation
        WHERE 1=1
    """
    params = []
    if zone:
        query += " AND zone = ?"
        params.append(zone)
    query += f" GROUP BY {date_trunc}, zone ORDER BY periode, zone"

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df.to_dict(orient="records")


@app.get("/meteo", tags=["Data Science"])
def get_meteo(
    zone: str = Query(None, description="Zone géographique"),
    date_debut: str = Query(None),
    date_fin: str = Query(None),
    limit: int = Query(1000, le=10000),
):
    """Données météo par zone — pour corréler avec la consommation (modèle ML)."""
    conn = get_db()
    query = "SELECT * FROM meteo WHERE 1=1"
    params = []
    if zone:
        query += " AND zone = ?"
        params.append(zone)
    if date_debut:
        query += " AND date >= ?"
        params.append(date_debut)
    if date_fin:
        query += " AND date <= ?"
        params.append(date_fin)
    query += f" LIMIT {limit}"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df.to_dict(orient="records")


@app.get("/journaux-securite", tags=["Cybersécurité"])
def get_journaux_securite(
    systeme: str = Query(None, description="portail_client | plateforme_data | scada | ..."),
    type_evenement: str = Query(None, description="connexion_echouee | acces_refuse | ..."),
    limit: int = Query(1000, le=10000),
):
    """Journaux de sécurité — pour l'analyse SIEM de Harif (Cybersécurité)."""
    conn = get_db()
    query = "SELECT * FROM journaux_securite WHERE 1=1"
    params = []
    if systeme:
        query += " AND systeme = ?"
        params.append(systeme)
    if type_evenement:
        query += " AND type_evenement = ?"
        params.append(type_evenement)
    query += f" LIMIT {limit}"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df.to_dict(orient="records")
