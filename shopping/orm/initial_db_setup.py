import logging

from shopping.models import BulkDiscount, BundledProduct, Product, ProductDiscount
from shopping.orm.db_handler import DbHandler
from shopping.orm.setup import close_session, create_database

log = logging.getLogger(__name__)


def setup_database(scratch: bool = True) -> None:
    """
    A helper function to populate the initial db state.

    Parameters
    ----------
    scratch: To create db from scratch or not.
    """
    create_database(scratch=scratch)

    db_handler = DbHandler()

    try:
        # Add initial 4 products
        p1 = db_handler.create(Product(sku="ipd", name="Super iPad", unit_price=549.99))
        p2 = db_handler.create(Product(sku="mbp", name="MacBook Pro", unit_price=1399.99))
        p3 = db_handler.create(Product(sku="atv", name="Apple TV", unit_price=109.50))
        p4 = db_handler.create(Product(sku="vga", name="VGA adapter", unit_price=30.00))

        # Add initial discount policies
        # Add product discount
        db_handler.create(ProductDiscount(product_id=p3.id, new_price_ratio=2 / 3, minimum_units=3, is_active=True))

        # Add bulk discount
        db_handler.create(BulkDiscount(product_id=p1.id, minimum_units=5, new_unit_price=499.99, is_active=True))

        # Add bundled prodcut
        db_handler.create(BundledProduct(product_id=p2.id, bundled_product_id=p4.id, is_active=True))

    finally:
        close_session()

    log.info("Populated the database with initial values.")
