# app/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.init_db import init_db
from app.routers.health import router as health_router
from app.routers.habits import router as habits_router
from app.routers.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown (nothing to clean up yet)


app = FastAPI(
    title="HabitOS",
    version="0.1.0",
    description="Habit OS API - Track and manage your habits effectively.",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(habits_router)
app.include_router(users_router)
