from typing import Optional
from fastapi import FastAPI
import uvicorn
import os

from worker import process_item
from item import Item

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
  return Item(id=item_id, quantity=1, price=10.0)

@app.post("/items")
async def add_item(item: Item):
  process_item.delay(id=item.id, price=item.price, quantity=item.quantity)
  return {"message": "Item received"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    reload = os.getenv("ENV") == "dev"
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info", reload=True)