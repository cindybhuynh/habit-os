# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.health import router as health_router
from app.routers.habits import router as habits_router
from app.routers.users import router as users_router
from app.routers.completions import router as completions_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="HabitOS",
    version="0.1.0",
    description="Habit OS API - Track and manage your habits effectively.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(habits_router)
app.include_router(users_router)
app.include_router(completions_router)
