# -*- coding: utf-8 -*-

import pandas as pd
import sqlite3
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "donnees")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "neovolt.db")


def load_csv(filename):
    path = os.path.join(DATA_DIR, filename)
    print(f"chargement {filename}...")
    return pd.read_csv(path, low_memory=False)


def clean_releves(df):
    avant = len(df)
    df = df.drop_duplicates()
    df = df[df["consommation_kwh"].notna()]
    df = df[df["consommation_kwh"] >= 0]
    p99 = df["consommation_kwh"].quantile(0.99)
    df = df[df["consommation_kwh"] <= p99]
    print(f"  nettoyage : {avant} -> {len(df)} lignes")
    return df


def ingest():
    conn = sqlite3.connect(DB_PATH)

    fichiers = {
        "releves_consommation": ("releves_consommation.csv", clean_releves),
        "clients": ("clients.csv", None),
        "compteurs": ("compteurs.csv", None),
        "incidents_reseau": ("incidents_reseau.csv", None),
        "cas_fraude_confirmes": ("cas_fraude_confirmes.csv", None),
        "meteo": ("meteo.csv", None),
        "journaux_securite": ("journaux_securite.csv", None),
        "actifs_si": ("actifs_si.csv", None),
    }

    for table, (fichier, cleaner) in fichiers.items():
        try:
            df = load_csv(fichier)
            if cleaner:
                df = cleaner(df)
            df.to_sql(table, conn, if_exists="replace", index=False)
            print(f"  {table} : {len(df)} lignes OK")
        except FileNotFoundError:
            print(f"  fichier manquant : {fichier}")

    conn.close()
    print(f"\nbase de donnees creee : {DB_PATH}")


if __name__ == "__main__":
    ingest()
