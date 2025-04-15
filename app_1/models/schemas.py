from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., example="apple")
    price: float = Field(..., gt=0, example=3.5)
    description: str = Field(None, example="Fresh and juicy")