from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import stats
from app.routers import user

app = FastAPI()

app.include_router(stats.router)
app.include_router(user.router)
app.mount("/", StaticFiles(directory="public", html=True), name="public")