from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.habits import router as habits_router
from app.routers.users import router as users_router
from app.db.init_db import init_db

app = FastAPI(
    title="HabitOS",
    version="0.1.0",
    description="Habit OS API - Track and manage your habits effectively.",
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(health_router)
app.include_router(habits_router)
app.include_router(users_router)
