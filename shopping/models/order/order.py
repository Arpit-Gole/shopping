"""
A class to represent an order.
"""

from datetime import date

from sqlalchemy import Column, Date, Float, Integer
from sqlalchemy.orm import Mapped, relationship

from shopping.models.base import Auditing
from shopping.models.order.order_line_item import OrderLineItem


class Order(Auditing):
    __tablename__ = "orders"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    order_date: Date = Column(Date, default=date.today, nullable=False)
    total_amount: float = Column(Float, default=0.0, nullable=False)
    discount_amount: float = Column(Float, default=0.0, nullable=False)
    final_amount: float = Column(Float, default=0.0, nullable=False)

    line_items: Mapped[list[OrderLineItem]] = relationship("OrderLineItem", back_populates="order")

    def total_number_of_products(self) -> int:
        """
        To calculate the total number of products in the order.
        """
        count = 0
        for oli in self.line_items:
            count += oli.quantity
        return count
