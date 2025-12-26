from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.habits import router as habits_router


app = FastAPI(title="HabitOS")

app.include_router(health_router)
app.include_router(habits_router)

@app.get("/hello")
async def say_hello():
    return {"Hello": "World"}