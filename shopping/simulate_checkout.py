"""
A module to simulate the checkout workflow.
"""
from prettytable import PrettyTable

from shopping.models import Product
from shopping.orm.db_handler import DbHandler


class SimulateCheckout:
    def __init__(self) -> None:
        self.db_handler = DbHandler()

    def simulate(self) -> list[int]:
        print("######################################################")  # noqa: T201
        print("Welcome to the shopping chart")  # noqa: T201
        print("######################################################")  # noqa: T201
        print("\n")  # noqa: T201
        print("We have the following products available:")  # noqa: T201

        # To display in console create a table
        table = PrettyTable()
        table.field_names = ["Id", "SKU", "Name", "Price"]

        for product in self.db_handler.read_all(model=Product):
            table.add_row([product.id, product.sku, product.name, product.unit_price])

        print(table)  # noqa: T201

        print("\n")  # noqa: T201

        return self.capture_valid_product_ids(
            products_to_purchase=list(map(int, input("Enter comma-separated product Id to " "purchase:").split(",")))
        )

    def capture_valid_product_ids(self, products_to_purchase: list[int]) -> list[int]:
        """
        A helper function to filter the user input.

        Parameters
        ----------
        products_to_purchase: A list of user entered product ids.

        Returns
        -------
        A list of valid products to purchase.
        """
        # Fetch all the valid products
        valid_product_ids = []
        for product in self.db_handler.read_all(model=Product):
            valid_product_ids.append(product.id)

        valid_products_to_purchase = []
        for product in products_to_purchase:
            if product in valid_product_ids:
                valid_products_to_purchase.append(product)

        return valid_products_to_purchase
