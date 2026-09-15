import logging
from typing import List, Optional

# Настраиваем базовое логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class Product:
    """Класс для представления продукта."""

    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        logging.info(f"Продукт успешно инициализирован: {self.name}")


class Category:
    """Класс для представления категории продуктов."""

    # Атрибуты класса для подсчета общего количества категорий и уникальных товаров
    category_count: int = 0
    product_count: int = 0

    name: str
    description: str
    products: List[Product]

    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None) -> None:
        self.name = name
        self.description = description
        self.products = products if products is not None else []

        # Автоматически увеличиваем счетчик категорий при создании нового объекта
        Category.category_count += 1

        # Подсчитываем количество уникальных товаров, добавленных в эту категорию
        Category.product_count += len(self.products)
        logging.info(f"Категория успешно инициализирована: {self.name}")
