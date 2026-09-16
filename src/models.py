import logging
import sys
from typing import Any

# Настройка логирования с явным указанием обычного потока вывода sys.stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)


class Product:
    """Класс для представления продукта."""

    name: str
    description: str
    _price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity
        logging.info(f"Продукт успешно инициализирован: '{self.name}'")

    def __str__(self) -> str:
        """Возвращает строковое представление продукта."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: Any) -> float:
        """Складывает общую стоимость двух продуктов на складе (цена * количество)."""
        if not isinstance(other, Product):
            logging.error(f"Попытка сложения Product с объектом другого типа: {type(other)}")
            raise TypeError("Складывать можно только объекты класса Product")

        total_cost = (self.price * self.quantity) + (other.price * other.quantity)
        logging.info(f"Выполнено сложение продуктов '{self.name}' и '{other.name}'. Результат: {total_cost} руб.")
        return total_cost

    @classmethod
    def new_product(cls, product_data: dict[str, Any], current_products: list["Product"] | None = None) -> "Product":
        """Фабричный метод для создания продукта из словаря."""
        name = product_data["name"]
        description = product_data["description"]
        price = product_data["price"]
        quantity = product_data["quantity"]

        if current_products:
            for existing_product in current_products:
                if existing_product.name.lower() == name.lower():
                    existing_product.quantity += quantity
                    existing_product.price = max(existing_product.price, price)
                    logging.info(f"Обновлен существующий продукт-дубликат: '{existing_product.name}'")
                    return existing_product

        return cls(name, description, price, quantity)

    @property
    def price(self) -> float:
        """Геттер для получения цены продукта."""
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для изменения цены."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self._price:
            user_answer = input(
                f"Вы уверены, что хотите понизить цену для {self.name} "
                f"с {self._price} руб. до {new_price} руб.? (y/n): "
            )
            if user_answer.lower() != "y":
                print("Действие отменено.")
                return

        self._price = new_price


class Category:
    """Класс для представления категории продуктов."""

    category_count: int = 0
    product_count: int = 0

    name: str
    description: str
    __products: list[Product]

    def __init__(self, name: str, description: str, products: list[Product] | None = None) -> None:
        self.name = name
        self.description = description
        self.__products = []
        Category.category_count += 1

        if products is not None:
            for product in products:
                self.add_product(product)

        logging.info(f"Категория успешно инициализирована: '{self.name}'")

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в приватный список товаров категории."""
        self.__products.append(product)
        Category.product_count += 1
        logging.info(f"В категорию '{self.name}' добавлен продукт: '{product.name}'")

    def __str__(self) -> str:
        """Возвращает строковое представление категории с подсчетом количества всех товаров."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    @property
    def products(self) -> str:
        """Возвращает строковое представление продуктов в категории."""
        result = []
        for product in self.__products:
            result.append(f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.")
        return "\n".join(result)


class CategoryIterator:
    """Класс-итератор для поочередного перебора объектов продуктов в категории."""

    category_products: list[Product]
    index: int

    def __init__(self, category_obj: Category) -> None:

        self.category_products = category_obj.__dict__.get(f"_{Category.__name__}__products", [])
        self.index = 0
        logging.info(f"Создан итератор для категории '{category_obj.name}'")

    def __iter__(self) -> "CategoryIterator":
        return self

    def __next__(self) -> Product:
        if self.index < len(self.category_products):
            product = self.category_products[self.index]
            self.index += 1
            return product
        else:
            logging.info("Итерация по категории завершена.")
            raise StopIteration
