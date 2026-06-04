from fastapi import FastAPI, Query, HTTPException
import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "neovolt.db")

app = FastAPI(title="Neovolt Grid+ API", version="1.0.0")


def get_db():
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=503, detail="base de donnees introuvable, lancer ingestion.py d'abord")
    return sqlite3.connect(DB_PATH)


@app.get("/")
def root():
    return {"api": "Neovolt Grid+", "docs": "/docs"}


@app.get("/releves")
def get_releves(
    zone: str = Query(None),
    date_debut: str = Query(None),
    date_fin: str = Query(None),
    limit: int = Query(1000, le=10000),
):
    conn = get_db()
    q = "SELECT * FROM releves_consommation WHERE 1=1"
    params = []
    if zone:
        q += " AND zone = ?"
        params.append(zone)
    if date_debut:
        q += " AND date >= ?"
        params.append(date_debut)
    if date_fin:
        q += " AND date <= ?"
        params.append(date_fin)
    q += f" LIMIT {limit}"
    df = pd.read_sql_query(q, conn, params=params)
    conn.close()
    return df.to_dict(orient="records")


@app.get("/clients")
def get_clients(
    segment: str = Query(None),
    limit: int = Query(500, le=5000),
):
    conn = get_db()
    q = "SELECT * FROM clients WHERE 1=1"
    params = []
    if segment:
        q += " AND segment = ?"
        params.append(segment)
    q += f" LIMIT {limit}"
    df = pd.read_sql_query(q, conn, params=params)
    conn.close()
    return df.to_dict(orient="records")


@app.get("/incidents")
def get_incidents(
    zone: str = Query(None),
    type_incident: str = Query(None),
    limit: int = Query(500, le=5000),
):
    conn = get_db()
    q = "SELECT * FROM incidents_reseau WHERE 1=1"
    params = []
    if zone:
        q += " AND zone = ?"
        params.append(zone)
    if type_incident:
        q += " AND type = ?"
        params.append(type_incident)
    q += f" LIMIT {limit}"
    df = pd.read_sql_query(q, conn, params=params)
    conn.close()
    return df.to_dict(orient="records")


@app.get("/fraudes")
def get_fraudes(type_fraude: str = Query(None)):
    conn = get_db()
    q = "SELECT * FROM cas_fraude_confirmes WHERE 1=1"
    params = []
    if type_fraude:
        q += " AND type_fraude = ?"
        params.append(type_fraude)
    df = pd.read_sql_query(q, conn, params=params)
    conn.close()
    return df.to_dict(orient="records")


@app.get("/stats/conso")
def get_stats_conso(
    zone: str = Query(None),
    granularite: str = Query("jour"),
):
    conn = get_db()
    if granularite == "mois":
        d = "strftime('%Y-%m', date)"
    elif granularite == "semaine":
        d = "strftime('%Y-%W', date)"
    else:
        d = "date"

    q = f"""
        SELECT {d} as periode, zone,
            COUNT(*) as nb,
            ROUND(AVG(consommation_kwh), 2) as moy,
            ROUND(SUM(consommation_kwh), 2) as total
        FROM releves_consommation WHERE 1=1
    """
    params = []
    if zone:
        q += " AND zone = ?"
        params.append(zone)
    q += f" GROUP BY {d}, zone ORDER BY periode"

    df = pd.read_sql_query(q, conn, params=params)
    conn.close()
    return df.to_dict(orient="records")


@app.get("/meteo")
def get_meteo(
    zone: str = Query(None),
    date_debut: str = Query(None),
    date_fin: str = Query(None),
    limit: int = Query(1000, le=10000),
):
    conn = get_db()
    q = "SELECT * FROM meteo WHERE 1=1"
    params = []
    if zone:
        q += " AND zone = ?"
        params.append(zone)
    if date_debut:
        q += " AND date >= ?"
        params.append(date_debut)
    if date_fin:
        q += " AND date <= ?"
        params.append(date_fin)
    q += f" LIMIT {limit}"
    df = pd.read_sql_query(q, conn, params=params)
    conn.close()
    return df.to_dict(orient="records")


@app.get("/journaux-securite")
def get_journaux(
    systeme: str = Query(None),
    type_evenement: str = Query(None),
    limit: int = Query(1000, le=10000),
):
    conn = get_db()
    q = "SELECT * FROM journaux_securite WHERE 1=1"
    params = []
    if systeme:
        q += " AND systeme = ?"
        params.append(systeme)
    if type_evenement:
        q += " AND type_evenement = ?"
        params.append(type_evenement)
    q += f" LIMIT {limit}"
    df = pd.read_sql_query(q, conn, params=params)
    conn.close()
    return df.to_dict(orient="records")
