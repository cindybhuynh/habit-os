from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.habits import router as habits_router


app = FastAPI(
    title="HabitOS",
    version="0.1.0",
    description="Habit OS API - Track and manage your habits effectively.",
)

app.include_router(health_router)
app.include_router(habits_router)