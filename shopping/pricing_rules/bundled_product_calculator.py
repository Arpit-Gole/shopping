"""
A class to apply all the Bundled discounts pricing rules
"""

import logging

from shopping.models import BundledProduct, Order, OrderLineItem, Product
from shopping.orm.db_handler import DbHandler

log = logging.getLogger(__name__)


class BundledProductCalculator:
    def __init__(self) -> None:
        self.db_handler = DbHandler()

    def process(self, order: Order) -> Order:
        # process each line items
        for oli in order.line_items:
            log.info("Applying bundled discounts on each order line item.")

            bundled_products = self.db_handler.read_by_filter(
                model=BundledProduct, filters={"product_id": oli.product_id, "is_active": True}
            )

            # Calculate the discount amount on the order.
            # We expect only 1 offer type is active at a time on a product.
            # Whereas in real life there might be multiple. Then requires
            # processing logic.
            if bundled_products:
                bundled_product_details = self.db_handler.read_by_id(
                    model=Product, record_id=bundled_products[0].bundled_product_id
                )

                # 1. If bundled product already present in the order:
                for inner_oli in order.line_items:
                    if bundled_products[0].bundled_product_id == inner_oli.product_id:
                        # Case 1: Both already equally present.
                        if oli.quantity == inner_oli.quantity:
                            order.discount_amount += oli.quantity * bundled_product_details.unit_price

                        # Case 2: More bundled product already present.
                        if oli.quantity < inner_oli.quantity:
                            order.discount_amount += oli.quantity * bundled_product_details.unit_price

                        # Case 3: Less bundled product already present.
                        if oli.quantity > inner_oli.quantity:
                            # 3.1. Calculate the difference
                            difference = oli.quantity - inner_oli.quantity
                            oli.quantity += difference
                            # 3.2. Update the total amount
                            order.total_amount += difference * bundled_product_details.unit_price
                            # 3.3. Give the discount for the added products.
                            order.discount_amount += inner_oli.quantity * bundled_product_details.unit_price

                # 2. If bundled product is not present in the order
                # 2.1 Add the product as a line item.
                order.line_items.append(
                    OrderLineItem(product_id=bundled_products[0].bundled_product_id, quantity=oli.quantity)
                )
                # 2.2 Update the total amount
                order.total_amount += oli.quantity * bundled_product_details.unit_price
                # 2.3. Give the discount for the added products.
                order.discount_amount += oli.quantity * bundled_product_details.unit_price

        log.info("Applied bulk discounts on each order line item")

        return order
