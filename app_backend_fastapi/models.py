from sqlalchemy import Column, Integer, String, Text, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    link_product = Column(String(255), nullable=False)  # Обязательное поле
    name_product = Column(String(255), nullable=True, default=None)
    description = Column(Text, nullable=True, default=None)
    rate = Column(DECIMAL(10, 2), nullable=True, default=None)

    price_histories = relationship("PriceHistory", back_populates="product")

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    price = Column(DECIMAL(10, 2), nullable=False)
    price_time = Column(TIMESTAMP, nullable=False)

    product = relationship("Product", back_populates="price_histories")
