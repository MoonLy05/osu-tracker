from fastapi import APIRouter
from app.services.ossapi import api, usuario
from app.database import leer_daily_challenges

router = APIRouter()

def construir_daily_challenge(dc):
    return {
        "momento": dc['momento'],
        "daily_streak_current": dc['daily_streak_current'],
        "daily_streak_best": dc['daily_streak_best'],
        "weekly_streak_current": dc['weekly_streak_current'],
        "weekly_streak_best": dc['weekly_streak_best'],
        "playcount": dc['playcount'],
        "top_10p_placements": dc['top_10p_placements'],
        "top_50p_placements": dc['top_50p_placements']
    }

def construir_usuario(user_data):
    return {
        "username": user_data.username,
        "avatar_url": user_data.avatar_url,
        "cover_url": user_data.cover_url,
        "country_code": user_data.country_code,
        "is_supporter": user_data.is_supporter,
        "has_supported": user_data.has_supported,
        "join_date": user_data.join_date.isoformat() if user_data.join_date else None,
    }

@router.get("/user")
def get_user():
    user_data = api.user(usuario)
    return construir_usuario(user_data)

@router.get("/daily_challenges")
def get_daily_challenges():
    daily_challenges = leer_daily_challenges()
    return [construir_daily_challenge(dc) for dc in daily_challenges]