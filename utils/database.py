# Importa json para leer archivos en formato JSON
import json

# Importa sqlite3 para conectarse a bases de datos SQLite
import sqlite3

# Importa Path para trabajar con rutas de archivos
from pathlib import Path

# Importa Iterable para tipado de colecciones iterables
from typing import Iterable

# Importa pandas para manejar DataFrames
import pandas as pd

# Importa numpy para manejo de datos numéricos
import numpy as np

# Importa rutas y nombres de bases de datos desde config
from config import DATA_DIR, STATS_DB_CANDIDATES, GPS_DB_CANDIDATES


# Función que devuelve la primera base de datos existente entre varias candidatas
def _resolve_db(candidates: Iterable[Path]) -> Path:
    for candidate in candidates:
        if Path(candidate).exists():
            return Path(candidate)

    # Lanza error si no encuentra ninguna base válida
    raise FileNotFoundError(f"No se encontró ninguna base de datos entre: {list(candidates)}")


# Función que abre conexión con la base de datos de estadísticas
def get_stats_connection():
    return sqlite3.connect(_resolve_db(STATS_DB_CANDIDATES))


# Función que abre conexión con la base de datos GPS
def get_gps_connection():
    return sqlite3.connect(_resolve_db(GPS_DB_CANDIDATES))


# Función que lista las tablas disponibles en una conexión SQLite
def _list_tables(conn) -> list[str]:
    query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    return pd.read_sql_query(query, conn)["name"].tolist()


# Función que lee la primera tabla existente entre varias candidatas
def _read_first_existing(conn, table_candidates: list[str]) -> pd.DataFrame:
    tables = set(_list_tables(conn))

    for table in table_candidates:
        if table in tables:
            return pd.read_sql_query(f'SELECT * FROM "{table}"', conn)

    # Lanza error si no encuentra ninguna tabla válida
    raise ValueError(f"No se encontró ninguna tabla válida. Candidatas: {table_candidates}. Disponibles: {sorted(tables)}")


# Función que normaliza el DataFrame de performance
def normalize_performance_df(df: pd.DataFrame) -> pd.DataFrame:

    # Renombra columnas a nombres más claros
    rename_map = {
        "Gls": "Goles",
        "As": "Asistencias",
        "VelMax_kmh": "VelMax",
    }
    df = df.rename(columns=rename_map).copy()

    # Crea columnas obligatorias si faltan
    required_defaults = {
        "Nombre": "", "Equipo": "", "Posición": "Sin dato", "Edad": 0,
        "xG": 0, "Goles": 0, "Asistencias": 0, "Rem": 0, "RegCmp": 0,
        "DnG": 0, "Recuperaciones": 0, "PJ": 0, "VelMax": 0, "Distancia_km": 0,
    }
    for col, default in required_defaults.items():
        if col not in df.columns:
            df[col] = default

    # Convierte columnas numéricas a formato numérico seguro
    numeric_cols = ["Edad", "xG", "Goles", "Asistencias", "Rem", "RegCmp", "DnG", "Recuperaciones", "PJ", "VelMax", "Distancia_km"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


# Función que normaliza el DataFrame GPS
def normalize_gps_df(df: pd.DataFrame) -> pd.DataFrame:

    # Renombra columnas a nombres consistentes
    rename_map = {
        "TipoSesion": "Tipo",
        "Sprints_n": "Sprints",
        "Acel_Alta_n": "Acel_Alta",
        "Decel_Alta_n": "Decel_Alta",
        "Minutos Totales": "Minutos",
    }
    df = df.rename(columns=rename_map).copy()

    # Convierte la fecha a datetime si existe
    if "Fecha" in df.columns:
        df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
    else:
        df["Fecha"] = pd.NaT

    # Asegura columnas de texto básicas
    for col in ["Jugadora", "Tipo", "Mes"]:
        if col not in df.columns:
            df[col] = ""

    # Asegura columnas numéricas obligatorias
    required_numeric = ["DistTotal_m", "DistAltaVel_m", "Sprints", "Acel_Alta", "Decel_Alta", "CargaMetabolica", "DistPorMin", "Minutos"]
    for col in required_numeric:
        if col not in df.columns:
            df[col] = 0
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Estima minutos si faltan pero hay distancia y distancia por minuto
    if (df["Minutos"] == 0).all() and "DistPorMin" in df.columns and "DistTotal_m" in df.columns:

        df["DistPorMin"] = pd.to_numeric(df["DistPorMin"], errors="coerce")
        df["DistPorMin"] = df["DistPorMin"].replace([np.inf, -np.inf], np.nan)

        df["DistTotal_m"] = pd.to_numeric(df["DistTotal_m"], errors="coerce")
        df["DistTotal_m"] = df["DistTotal_m"].replace([np.inf, -np.inf], np.nan)

        valid_mask = df["DistPorMin"] > 0
        df.loc[valid_mask, "Minutos"] = df.loc[valid_mask, "DistTotal_m"] / df.loc[valid_mask, "DistPorMin"]
        df["Minutos"] = df["Minutos"].fillna(0)

    return df


# Función que carga y normaliza los datos de performance
def get_performance_data() -> pd.DataFrame:
    with get_stats_connection() as conn:
        df = _read_first_existing(conn, ["stats_players", "liga_players_stats", "liga_players_stats_2526", "player_stats"])
    return normalize_performance_df(df)


# Función que carga los totales GPS
def get_gps_totals() -> pd.DataFrame:
    with get_gps_connection() as conn:
        df = _read_first_existing(conn, ["gps_global_totals", "gps_global_totals_2526"])
    return df


# Función que carga y normaliza la temporada GPS
def get_gps_season() -> pd.DataFrame:
    with get_gps_connection() as conn:
        df = _read_first_existing(conn, ["gps_full_season", "gps_full_season_2526"])
    return normalize_gps_df(df)


# Función que carga los glosarios de stats y GPS
def get_glossaries():
    glossaries = {}

    # Carga glosario de estadísticas
    with get_stats_connection() as conn_stats:
        glossaries["stats"] = _read_first_existing(conn_stats, ["glosario_stats", "stats_glossary"])

    # Carga glosario GPS
    with get_gps_connection() as conn_gps:
        glossaries["gps"] = _read_first_existing(conn_gps, ["glosario_gps", "gps_glossary"])

    return glossaries


# Función que carga los escudos guardados en base64
def load_shields_base64() -> dict:
    path = DATA_DIR / "shields_base64.json"

    # Si no existe el archivo, devuelve diccionario vacío
    if not path.exists():
        return {}

    # Lee el JSON de escudos
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# Función que devuelve la imagen base64 del escudo de un equipo
def get_shield_src(team_name: str | None) -> str | None:

    # Si no hay nombre de equipo, devuelve None
    if not team_name:
        return None

    shields = load_shields_base64()
    team = str(team_name).strip()

    # Busca el escudo con distintas extensiones posibles
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        key = f"{team}{ext}"
        if key in shields:
            return shields[key]

    return None