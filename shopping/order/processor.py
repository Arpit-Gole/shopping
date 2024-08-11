"""
A class to process an order.
"""

import logging
from collections import Counter

from shopping.models import Order, OrderLineItem, Product
from shopping.orm.db_handler import DbHandler
from shopping.pricing_rules import (
    BulkDiscountCalculator,
    BundledProductCalculator,
    ProductDiscountCalculator,
)

log = logging.getLogger(__name__)


class Processor:
    def __init__(self, products_to_purchase_ids: list[int]) -> None:
        self.products_to_purchase_ids = products_to_purchase_ids
        self.db_handler = DbHandler()

    @property
    def products_to_purchase_ids(self) -> list[int]:
        return self._products_to_purchase_ids

    @products_to_purchase_ids.setter
    def products_to_purchase_ids(self, value: list) -> None:
        if len(value) == 0:
            raise ValueError
        self._products_to_purchase_ids = value

    def process(self) -> Order:
        # 1. Create a new order to process.
        new_order = self.create_order()

        # 2. Calculate the price:- apply various pricing rules.
        new_order = ProductDiscountCalculator().process(order=new_order)

        new_order = BulkDiscountCalculator().process(order=new_order)

        new_order = BundledProductCalculator().process(order=new_order)

        # 3. Save the order.
        new_order = self.save_order(order=new_order)

        log.info("Order processed successfully.")
        return new_order

    def create_order(self) -> Order:
        """
        Creates an order object, which we'll later save.
        """

        new_order = Order(total_amount=0.0, discount_amount=0.0, final_amount=0.0)

        for product_id, quantity in dict(Counter(self.products_to_purchase_ids)).items():
            new_order.line_items.append(OrderLineItem(product_id=product_id, quantity=quantity))

            product_details = self.db_handler.read_by_id(model=Product, record_id=product_id)

            new_order.total_amount += product_details.unit_price * quantity

        return new_order

    def save_order(self, order: Order) -> Order:
        """
        Saves the order.
        Parameters
        ----------
        order: Order to process
        """
        # Final prep before saving.
        order.final_amount = order.total_amount - order.discount_amount

        return self.db_handler.create(order)
