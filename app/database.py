import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "osu_historial.db"


def inicializar_bd(conexion):
    conexion.executescript(
        """
        CREATE TABLE IF NOT EXISTS snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            momento TEXT,
            modo TEXT,
            pp REAL,
            global_rank INTEGER,
            country_rank INTEGER,
            nivel REAL,
            accuracy REAL,
            play_count INTEGER,
            play_time INTEGER,
            maximum_combo INTEGER
        );

        CREATE TABLE IF NOT EXISTS daily_challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            momento TEXT,
            daily_streak_current INTEGER,
            daily_streak_best INTEGER,
            weekly_streak_current INTEGER,
            weekly_streak_best INTEGER,
            playcount INTEGER,
            top_10p_placements INTEGER,
            top_50p_placements INTEGER
        );
        """
    )
    conexion.commit()


def get_conexion():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conexion = sqlite3.connect(DB_PATH)
    inicializar_bd(conexion)
    conexion.row_factory = sqlite3.Row
    return conexion

def leer_snapshots():
    conexion = get_conexion()
    filas = conexion.execute("SELECT * FROM snapshots").fetchall()
    conexion.close()
    return [dict(fila) for fila in filas]

def leer_snapshots_modo(modo):
    conexion = get_conexion()
    filas = conexion.execute(
        "SELECT * FROM snapshots WHERE modo = ? ORDER BY momento",
        (modo,)
    ).fetchall()
    conexion.close()
    return [dict(f) for f in filas]

def leer_daily_challenges():
    conexion = get_conexion()
    filas = conexion.execute("SELECT * FROM daily_challenges").fetchall()
    conexion.close()
    return [dict(fila) for fila in filas]

def guardar_snapshot(momento, modo, pp, global_rank, country_rank, nivel, accuracy, play_count, play_time, maximum_combo):
    conexion = get_conexion()
    conexion.execute(
        "INSERT INTO snapshots (momento, modo, pp, global_rank, country_rank, nivel, accuracy, play_count, play_time, maximum_combo) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (momento, modo, pp, global_rank, country_rank, nivel, accuracy, play_count, play_time, maximum_combo)
    )
    conexion.commit()
    conexion.close()
    
def guardar_daily_challenge(momento, daily_streak_current, daily_streak_best, weekly_streak_current, weekly_streak_best, playcount, top_10p_placements, top_50p_placements):
    conexion = get_conexion()
    conexion.execute(
        "INSERT INTO daily_challenges (momento, daily_streak_current, daily_streak_best, weekly_streak_current, weekly_streak_best, playcount, top_10p_placements, top_50p_placements) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (momento, daily_streak_current, daily_streak_best, weekly_streak_current, weekly_streak_best, playcount, top_10p_placements, top_50p_placements)
    )
    conexion.commit()
    conexion.close()
    
def leer_ultimo_daily_challenge():
    conexion = get_conexion()
    fila = conexion.execute(
        "SELECT * FROM daily_challenges ORDER BY momento DESC LIMIT 1"
    ).fetchone()
    conexion.close()
    return dict(fila) if fila else None
    
def ultima_snapshot(modo):
    conexion = get_conexion()
    fila = conexion.execute(
        "SELECT * FROM snapshots WHERE modo = ? ORDER BY momento DESC LIMIT 1", (modo,)
    ).fetchone()
    conexion.close()
    return dict(fila) if fila else None