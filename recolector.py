from app.services.ossapi import api, usuario, modos
from datetime import datetime
from app.database import guardar_snapshot, ultima_snapshot, leer_ultimo_daily_challenge, guardar_daily_challenge

ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
dc = api.user(usuario).daily_challenge_user_stats
ultima_dc = leer_ultimo_daily_challenge()
cambio_dc = ultima_dc is None or (
    ultima_dc['daily_streak_current'] != dc.daily_streak_current or
    ultima_dc['daily_streak_best'] != dc.daily_streak_best or
    ultima_dc['playcount'] != dc.playcount or
    ultima_dc['top_10p_placements'] != dc.top_10p_placements or
    ultima_dc['top_50p_placements'] != dc.top_50p_placements
)
if cambio_dc:
    guardar_daily_challenge(
        ahora, dc.daily_streak_current, dc.daily_streak_best,
        dc.weekly_streak_current, dc.weekly_streak_best,
        dc.playcount, dc.top_10p_placements, dc.top_50p_placements
    )

for modo in modos:
    user = api.user(usuario, mode=modo)
    s = user.statistics

    ultima = ultima_snapshot(modo)
    cambio = ultima is None or (
        ultima['pp'] != s.pp or
        ultima['global_rank'] != s.global_rank or
        ultima['country_rank'] != s.country_rank
    )

    if cambio:
        guardar_snapshot(ahora,
            modo, s.pp, s.global_rank, s.country_rank, s.level.current,
            s.accuracy, s.play_count, s.play_time, s.maximum_combo
        )