# -*- coding: utf-8 -*-
"""
Pipeline d'ingestion - Neovolt Grid+
"""

import pandas as pd
import sqlite3
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "donnees")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "neovolt.db")


def load_csv(filename):
    path = os.path.join(DATA_DIR, filename)
    print(f"  Chargement : {filename}")
    return pd.read_csv(path, low_memory=False)


def clean_releves(df):
    """Nettoyage des relevés de consommation."""
    avant = len(df)
    df = df.drop_duplicates()
    df = df[df["consommation_kwh"].notna()]
    df = df[df["consommation_kwh"] >= 0]
    p99 = df["consommation_kwh"].quantile(0.99)
    df = df[df["consommation_kwh"] <= p99]
    apres = len(df)
    print(f"    Releves : {avant} -> {apres} lignes apres nettoyage")
    return df


def ingest():
    print("=== Néovolt Grid+ — Pipeline d'ingestion ===\n")

    conn = sqlite3.connect(DB_PATH)
    print(f"Base de données : {DB_PATH}\n")

    tables = {
        "releves_consommation": ("releves_consommation.csv", clean_releves),
        "clients": ("clients.csv", None),
        "compteurs": ("compteurs.csv", None),
        "incidents_reseau": ("incidents_reseau.csv", None),
        "cas_fraude_confirmes": ("cas_fraude_confirmes.csv", None),
        "meteo": ("meteo.csv", None),
        "journaux_securite": ("journaux_securite.csv", None),
        "actifs_si": ("actifs_si.csv", None),
    }

    for table_name, (filename, cleaner) in tables.items():
        try:
            df = load_csv(filename)
            if cleaner:
                df = cleaner(df)
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f"  OK : {table_name} ({len(df)} lignes)\n")
        except FileNotFoundError:
            print(f"  SKIP : {filename} non trouvé\n")

    conn.close()
    print("=== Ingestion terminée ===")
    print(f"Base de données prête : {DB_PATH}")


if __name__ == "__main__":
    ingest()
