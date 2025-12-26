from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    return item




























# from fastapi import FastAPI
# from pydantic import BaseModel
# from datetime import date

# class Item(BaseModel):
#     name: str
#     schedule_type: str
#     target_count: int
#     start_date: date
#     notes: str

# app = FastAPI()

# @app.post("/items/")
# async def create_item(item: Item): 
#     return item
    
