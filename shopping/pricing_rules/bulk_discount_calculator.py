"""
A class to apply all the Bullk discounts pricing rules
"""

import logging

from shopping.models import BulkDiscount, Order, Product
from shopping.orm.db_handler import DbHandler

log = logging.getLogger(__name__)


class BulkDiscountCalculator:
    def __init__(self) -> None:
        self.db_handler = DbHandler()

    def process(self, order: Order) -> Order:
        # process each line items
        for oli in order.line_items:
            log.info("Applying bulk discounts on each order line item.")

            bulk_discounts = self.db_handler.read_by_filter(
                model=BulkDiscount, filters={"product_id": oli.product_id, "is_active": True}
            )

            # Calculate the discount amount on the order.
            # We expect only 1 offer type is active at a time on a product.
            # Whereas in real life there might be multiple. Then requires
            # processing logic.
            if bulk_discounts and order.total_number_of_products() >= bulk_discounts[0].minimum_units:
                product_details = self.db_handler.read_by_id(model=Product, record_id=oli.product_id)

                # Calculate the difference
                new_unit_discount_price = product_details.unit_price - bulk_discounts[0].new_unit_price

                order.discount_amount += oli.quantity * new_unit_discount_price

        log.info("Applied bulk discounts on each order line item")

        return order
