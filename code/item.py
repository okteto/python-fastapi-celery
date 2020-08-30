from pydantic import BaseModel

class Item(BaseModel):
    id: int
    quantity: int
    price: float



