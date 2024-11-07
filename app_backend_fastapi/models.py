from sqlalchemy import Column, Integer, String, Text, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    """
    Модель продукта, представляющая запись в таблице `products`.

    Attributes:
        id (int): Уникальный идентификатор продукта.
        link_product (str): Ссылка на продукт (обязательное поле).
        name_product (str, optional): Название продукта.
        description (str, optional): Описание продукта.
        rate (float, optional): Рейтинг продукта.

    Relationships:
        price_histories (list[PriceHistory]): Связь с историей цен данного продукта.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    link_product = Column(String(255), nullable=False)  # Обязательное поле
    name_product = Column(String(255), nullable=True, default=None)
    description = Column(Text, nullable=True, default=None)
    rate = Column(DECIMAL(10, 2), nullable=True, default=None)

    price_histories = relationship("PriceHistory", back_populates="product")

class PriceHistory(Base):
    """
    Модель истории цен, представляющая запись в таблице `price_history`.

    Attributes:
        id (int): Уникальный идентификатор записи истории цен.
        product_id (int): Идентификатор продукта, к которому относится эта история цен.
        price (float): Цена продукта на момент времени.
        price_time (datetime): Время, когда была зафиксирована цена.

    Relationships:
        product (Product): Связь с продуктом, которому принадлежит эта история цен.
    """
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    price = Column(DECIMAL(10, 2), nullable=False)
    price_time = Column(TIMESTAMP, nullable=False)

    product = relationship("Product", back_populates="price_histories")
