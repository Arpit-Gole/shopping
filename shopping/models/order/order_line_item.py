"""
A class to represent the items in the order.
"""

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from shopping.models.base import Auditing


class OrderLineItem(Auditing):
    __tablename__ = "order_line_items"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    product_id: int = Column(Integer, ForeignKey("products.id"), nullable=False)
    order_id: int = Column(Integer, ForeignKey("orders.id"), nullable=False)
    quantity: int = Column(Integer, nullable=False)

    product = relationship("Product")
    order = relationship("Order", back_populates="line_items")
