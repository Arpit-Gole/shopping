"""
A class to represents various types of bulk discounts on a product.
"""

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from shopping.models.base import Auditing


class BulkDiscount(Auditing):
    __tablename__ = "bulk_discounts"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    product_id: int = Column(Integer, ForeignKey("products.id"), nullable=False)
    minimum_units: int = Column(Integer, nullable=False)
    new_unit_price: float = Column(Float, nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)

    product = relationship("Product")
