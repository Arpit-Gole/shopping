"""
Simulate the shopping experience.
"""
import argparse
import logging

from shopping.order.processor import Processor
from shopping.orm.initial_db_setup import setup_database
from shopping.orm.setup import check_if_db_exists
from shopping.simulate_checkout import SimulateCheckout
from shopping.utilities.exceptions import DbNotFoundError
from shopping.utilities.logger import get_default_logger
from shopping.utilities.run_modes import RunModes


def main() -> None:
    """
    Reads the supplied arguments and kicks off the workflow.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--setup",
        required=False,
        type=bool,
        default=False,
        help="Does the initial database setup to run the application.",
    )
    parser.add_argument(
        "--update",
        required=False,
        type=bool,
        default=False,
        help="Update the database to reflect new changes.",
    )
    parser.add_argument(
        "--run_mode",
        required=False,
        type=int,
        default=RunModes.PROD,
        help=f"Defines the run mode for the application. Available modes are -"
        f" {[run_mode.value for run_mode in RunModes]}",
    )

    args = parser.parse_args()

    execute(setup=args.setup, update=args.update, run_mode=RunModes(args.run_mode))


def execute(setup: bool, update: bool, run_mode: RunModes) -> None:
    """
    Kicks off the workflow.

    Parameters
    ----------
    setup: Does the initial database setup to run the application.
    update: Update the database to reflect new changes.
    run_mode: Defines the run mode of the application.

    """
    # Setting up the logging config for the project.
    if run_mode == RunModes.DEBUG:
        log = get_default_logger(level=logging.DEBUG)
    else:
        # Don't want to populate the console with logs.
        log = get_default_logger(level=logging.ERROR)

    if setup:
        log.info("Setting up the initial database.")
        setup_database()
    if update:
        # Assessment brief only tell to that the rules should be flexible.
        # Add workflow to update the rules, add products and more.
        pass
    else:
        if not check_if_db_exists():
            raise DbNotFoundError

    # 1. Simulate the scanning experience.
    products_to_purchase_ids = SimulateCheckout().simulate()

    # 2. Process the order.
    order_processor = Processor(products_to_purchase_ids=products_to_purchase_ids)
    order = order_processor.process()

    # 3. Print the price.
    print(f"\nTotal expected: ${order.final_amount}\n\n")  # noqa: T201
    log.info("Shopping is complete.")


if __name__ == "__main__":
    main()
