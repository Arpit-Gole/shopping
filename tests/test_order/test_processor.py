"""
A testing suite to test the order processor.
"""

import pytest

from shopping.order.processor import Processor
from shopping.orm.initial_db_setup import setup_database
from shopping.orm.setup import DATABASE_PATH, close_session
from shopping.simulate_checkout import SimulateCheckout


@pytest.fixture
def setup_and_remove_db():
    setup_database(scratch=False)
    yield
    close_session()
    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink(missing_ok=True)


def test_order_with_single_product_pass(setup_and_remove_db):
    products_to_purchase_ids = SimulateCheckout().capture_valid_product_ids(products_to_purchase=[2])
    order_processor = Processor(products_to_purchase_ids=products_to_purchase_ids)
    order = order_processor.process()

    assert order.total_amount == 1429.99
    assert order.discount_amount == 30.0
    assert order.final_amount == 1399.99
    assert len(order.line_items) == 2


def test_order_with_single_product_fail(setup_and_remove_db):
    with pytest.raises(ValueError):
        products_to_purchase_ids = SimulateCheckout().capture_valid_product_ids(products_to_purchase=[1000])
        order_processor = Processor(products_to_purchase_ids=products_to_purchase_ids)
        order = order_processor.process()  # noqa: F841


def test_given_tc1_pass(setup_and_remove_db):
    products_to_purchase_ids = SimulateCheckout().capture_valid_product_ids(products_to_purchase=[3, 3, 3, 4])
    order_processor = Processor(products_to_purchase_ids=products_to_purchase_ids)
    order = order_processor.process()

    assert order.final_amount == 249.00


def test_given_tc2_pass(setup_and_remove_db):
    products_to_purchase_ids = SimulateCheckout().capture_valid_product_ids(products_to_purchase=[3, 1, 1, 3, 1, 1, 1])
    order_processor = Processor(products_to_purchase_ids=products_to_purchase_ids)
    order = order_processor.process()

    assert order.final_amount == 2718.95


def test_given_tc3_pass(setup_and_remove_db):
    products_to_purchase_ids = SimulateCheckout().capture_valid_product_ids(products_to_purchase=[2, 4, 1])
    order_processor = Processor(products_to_purchase_ids=products_to_purchase_ids)
    order = order_processor.process()

    assert order.final_amount == 1949.98
