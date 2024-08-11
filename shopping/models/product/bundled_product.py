"""
A class to represents various types of bundled products applied to a
product.
"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from shopping.models.base import Auditing


class BundledProduct(Auditing):
    __tablename__ = "bundled_products"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    product_id: int = Column(Integer, ForeignKey("products.id"), nullable=False)
    bundled_product_id: int = Column(Integer, ForeignKey("products.id"), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)

    product = relationship("Product", foreign_keys=[product_id])
    bundled_product = relationship("Product", foreign_keys=[bundled_product_id])
