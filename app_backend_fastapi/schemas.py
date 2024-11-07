from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class PriceHistoryBase(BaseModel):
    """
    Базовая модель истории цен.

    Attributes:
        price (float): Цена продукта.
        price_time (datetime): Время, когда была зафиксирована цена.
    """
    price: float
    price_time: datetime

class ProductBase(BaseModel):
    """
    Базовая модель продукта без идентификатора.

    Attributes:
        link_product (str): Ссылка на продукт.
        name_product (Optional[str]): Название продукта (необязательное).
        description (Optional[str]): Описание продукта (необязательное).
        rate (Optional[float]): Рейтинг продукта (необязательный).
    """
    link_product: str
    name_product: Optional[str] = None
    description: Optional[str] = None
    rate: Optional[float] = None

class ProductCreate(ProductBase):
    """
    Модель для создания нового продукта, 
    наследующая от базовой модели продукта.
    """
    pass

class Product(ProductBase):
    """
    Полная модель продукта с идентификатором и историей цен.

    Attributes:
        id (int): Уникальный идентификатор продукта.
        price_histories (List[PriceHistoryBase]): Список историй цен для продукта.
    """
    id: int
    price_histories: List[PriceHistoryBase] = []

    class Config:
        from_attributes = True
