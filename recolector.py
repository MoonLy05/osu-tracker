import ossapi, os, sqlite3
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

api = ossapi.Ossapi(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))

usuario = os.getenv("USERNAME")
modos = ["osu", "mania"]

conexion = sqlite3.connect("osu_historial.db")
cursor = conexion.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS snapshots (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        momento        TEXT,
        modo           TEXT,
        pp             REAL,
        global_rank    INTEGER,
        country_rank   INTEGER,
        nivel          INTEGER,
        accuracy       REAL,
        play_count     INTEGER,
        play_time      INTEGER,
        maximum_combo  INTEGER
    )
""")

for modo in modos:
    cuenta = api.user(usuario, mode=modo)
    s = cuenta.statistics

    cursor.execute(
        "SELECT pp, global_rank, country_rank FROM snapshots "
        "WHERE modo = ? ORDER BY momento DESC LIMIT 1",
        (modo,)
    )
    ultimo = cursor.fetchone()

    cambio = (
        ultimo is None
        or ultimo[0] != s.pp
        or ultimo[1] != s.global_rank
        or ultimo[2] != s.country_rank
    )

    if cambio:
        cursor.execute("""
            INSERT INTO snapshots
            (momento, modo, pp, global_rank, country_rank, nivel,
             accuracy, play_count, play_time, maximum_combo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(timespec="seconds"), modo,
            s.pp, s.global_rank, s.country_rank, s.level.current,
            s.accuracy, s.play_count, s.play_time, s.maximum_combo
        ))
        print(f"Cambio en {modo}: {s.pp:.0f}pp, Global #{s.global_rank}, Mexico #{s.country_rank} -> guardado {datetime.now().isoformat(timespec='seconds')}")
    else:
        print(f"Sin cambios en {modo}, no se guarda nada {datetime.now().isoformat(timespec='seconds')}")
        
conexion.commit()
conexion.close()