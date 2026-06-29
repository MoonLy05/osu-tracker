from fastapi import APIRouter
from app.database import leer_snapshots, leer_snapshots_modo

router = APIRouter()

@router.get("/stats")
def get_historial():
    return leer_snapshots()

@router.get("/stats/{modo}")
def get_historial_modo(modo: str):
    return leer_snapshots_modo(modo)