import json
import os
from typing import Any, List

from src.models import Category, Product


def load_products_from_json(file_path: str) -> List[Category]:
    """Загружает данные из JSON-файла и инициализирует объекты классов Category и Product."""
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        data: List[dict[str, Any]] = json.load(file)

    categories: List[Category] = []
    for category_data in data:
        products_list: List[Product] = []
        for product_data in category_data.get("products", []):
            product = Product(
                name=product_data["name"],
                description=product_data["description"],
                price=product_data["price"],
                quantity=product_data["quantity"],
            )
            products_list.append(product)

        category = Category(
            name=category_data["name"],
            description=category_data["description"],
            products=products_list,
        )
        categories.append(category)

    return categories
