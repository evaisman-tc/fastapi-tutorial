from typing import Set, Optional, List
from pydantic import BaseModel, Field, HttpUrl


class Image(BaseModel):
  url: HttpUrl
  name: str


class Item(BaseModel):
  name: str
  description: Optional[str] = Field(
      None, title="The description of the item", max_length=300
  )
  price: float = Field(..., gt=0,
                       description="The price must be greater than zero")
  tax: Optional[float] = 10.5
  tags: Set[str] = set()
  image: Optional[List[Image]] = None

  class Config:
      schema_extra = {
          "example": {
              "name": "Foo",
              "description": "A very nice Item",
              "price": 35.4,
              "tax": 3.2,
              "tags": { "test1", "test2" }
          }
      }


class Offer(BaseModel):
  name: str
  description: Optional[str] = None
  price: float
  items: List[Item]
