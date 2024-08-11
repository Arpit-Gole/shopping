"""
A class to apply all the Product discounts pricing rules
"""

import logging

from shopping.models import Order, Product, ProductDiscount
from shopping.orm.db_handler import DbHandler

log = logging.getLogger(__name__)


class ProductDiscountCalculator:
    def __init__(self) -> None:
        self.db_handler = DbHandler()

    def process(self, order: Order) -> Order:
        # process each line items
        for oli in order.line_items:
            log.info("Applying product discounts on each order line item.")

            product_discounts = self.db_handler.read_by_filter(
                model=ProductDiscount, filters={"product_id": oli.product_id, "is_active": True}
            )

            # Calculate the discount amount on the order.
            # We expect only 1 offer type is active at a time on a product.
            # Whereas in real life there might be multiple. Then requires
            # processing logic.
            if product_discounts:
                free_product_quantity = oli.quantity // product_discounts[0].minimum_units

                product_details = self.db_handler.read_by_id(model=Product, record_id=oli.product_id)

                order.discount_amount += free_product_quantity * product_details.unit_price

        log.info("Applied product discounts on each order line item")

        return order


# 1,1,1,1,2,2,2,3,3,3,3,3,3,3
