"""
A class to represent a product.
"""

from sqlalchemy import Column, Float, Integer, String

from shopping.models.base import Auditing


class Product(Auditing):
    __tablename__ = "products"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    sku: str = Column(String, nullable=False)
    name: str = Column(String, nullable=False)
    unit_price: float = Column(Float, nullable=False)
