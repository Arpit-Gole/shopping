"""
A class to represent various types of product discount.
"""

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from shopping.models.base import Auditing


class ProductDiscount(Auditing):
    __tablename__ = "product_discounts"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    product_id: int = Column(Integer, ForeignKey("products.id"), nullable=False)
    # The final ratio to be charged if the above product is present in
    # the minimum quantity.
    new_price_ratio: float = Column(Float, nullable=False)
    minimum_units: int = Column(Integer, nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)

    product = relationship("Product")
