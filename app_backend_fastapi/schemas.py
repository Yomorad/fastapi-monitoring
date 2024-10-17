from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class PriceHistoryBase(BaseModel):
    price: float
    price_time: datetime

class ProductBase(BaseModel):
    link_product: str
    name_product: Optional[str] = None
    description: Optional[str] = None
    rate: Optional[float] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    price_histories: List[PriceHistoryBase] = []

    class Config:
        from_attributes = True
