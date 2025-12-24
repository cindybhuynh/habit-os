from fastapi import FastAPI
from app.routers.health import router as health_router


app = FastAPI(title="HabitOS")

app.include_router(health_router)

@app.get("/hello")
async def say_hello():
    return {"Hello": "World"}