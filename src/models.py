import logging
import sys
from abc import ABC, abstractmethod
from typing import Any

# Настройка логгера для разделения потоков (INFO — sys.stdout, WARNING/ERROR — sys.stderr)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

if logger.hasHandlers():
    logger.handlers.clear()

log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

info_handler = logging.StreamHandler(sys.stdout)
info_handler.setLevel(logging.INFO)
info_handler.addFilter(lambda record: record.levelno <= logging.INFO)
info_handler.setFormatter(log_formatter)
logger.addHandler(info_handler)

error_handler = logging.StreamHandler(sys.stderr)
error_handler.setLevel(logging.WARNING)
error_handler.setFormatter(log_formatter)
logger.addHandler(error_handler)


# --- Абстрактные базовые классы ---


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов."""

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __add__(self, other: Any) -> float:
        pass


class AbstractStorage(ABC):
    """Абстрактный базовый класс для Категорий и Заказов."""

    @property
    @abstractmethod
    def products(self) -> Any:
        pass


# --- Класс-миксин ---


class PrintMixin:
    """Миксин для автоматического вывода информации о созданном объекте."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        print(repr(self))

    def __repr__(self) -> str:
        name = getattr(self, "name", "")
        description = getattr(self, "description", "")
        price = getattr(self, "price", 0.0)
        quantity = getattr(self, "quantity", 0)
        # Корректное формирование repr-строки: функции repr() передаются чистые атрибуты
        return f"{self.__class__.__name__}({repr(name)}, {repr(description)}, {price}, {quantity})"


# --- Основные классы продуктов ---


class Product(PrintMixin, BaseProduct):
    """Базовый класс для представления продукта."""

    name: str
    description: str
    _price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity
        super().__init__()

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: Any) -> float:
        if type(self) is not type(other):
            logging.error(f"Попытка сложения разных классов: " f"{type(self).__name__} и {type(other).__name__}")
            raise TypeError("Складывать можно только товары одного и того же класса")

        return (self.price * self.quantity) + (other.price * other.quantity)

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        self._price = new_price


class Smartphone(Product):
    """Класс-наследник для смартфонов."""

    efficiency: float
    model: str
    memory: int
    color: str

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color
        super().__init__(name, description, price, quantity)


class LawnGrass(Product):
    """Класс-наследник для газонной травы."""

    country: str
    germination_period: str
    color: str

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        self.country = country
        self.germination_period = germination_period
        self.color = color
        super().__init__(name, description, price, quantity)


class Category(AbstractStorage):
    """Класс для представления категории продуктов."""

    category_count: int = 0
    product_count: int = 0
    name: str
    description: str

    def __init__(self, name: str, description: str, products: list[Product] | None = None) -> None:
        self.name = name
        self.description = description
        self.__products: list[Product] = []
        Category.category_count += 1

        if products is not None:
            for product in products:
                self.add_product(product)

    def add_product(self, product: Any) -> None:
        if not isinstance(product, Product):
            logging.error(f"Попытка добавить некорректный объект: " f"{type(product).__name__}")
            raise TypeError("В категорию можно добавлять только продукты или их наследников")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> list[Product]:
        """Возвращает чистый список объектов (как нужно для len() в main.py)."""
        return self.__products

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."


class CategoryIterator:
    """Класс-итератор для поочередного перебора объектов продуктов в категории."""

    category_products: list[Product]
    index: int

    def __init__(self, category_obj: Category) -> None:
        self.category_products = category_obj.products
        self.index = 0

    def __iter__(self) -> "CategoryIterator":
        return self

    def __next__(self) -> Product:
        if self.index < len(self.category_products):
            product = self.category_products[self.index]
            self.index += 1
            return product
        else:
            raise StopIteration


# --- Класс Заказ ---


class Order(AbstractStorage):
    """Класс для оформления заказа на один тип товара."""

    product: Product
    quantity: int

    def __init__(self, product: Product, quantity: int) -> None:
        if not isinstance(product, Product):
            raise TypeError("Заказ можно оформить только на товар класса Product")
        self.product = product
        self.quantity = quantity
        logging.info(f"Оформлен заказ на {self.product.name} в количестве {self.quantity} шт.")

    @property
    def products(self) -> list[Product]:
        return [self.product]

    @property
    def total_cost(self) -> float:
        return self.product.price * self.quantity
