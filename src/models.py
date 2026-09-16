import logging
import sys
from typing import Any

# 1. Создаем корневой логгер
logger = logging.getLogger()
logger.setLevel(logging.INFO)


if logger.hasHandlers():
    logger.handlers.clear()

# Общий формат для всех логов
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# 2. Настраиваем обработчик для INFO (выводит только сообщения INFO в sys.stdout — белый цвет)
info_handler = logging.StreamHandler(sys.stdout)
info_handler.setLevel(logging.INFO)
# Фильтр, чтобы этот обработчик пропускал ТОЛЬКО уровень INFO и ниже
info_handler.addFilter(lambda record: record.levelno <= logging.INFO)
info_handler.setFormatter(log_formatter)
logger.addHandler(info_handler)

# 3. Настраиваем обработчик для ОШИБОК (выводит WARNING, ERROR и CRITICAL в sys.stderr — красный цвет)
error_handler = logging.StreamHandler(sys.stderr)
error_handler.setLevel(logging.WARNING)
error_handler.setFormatter(log_formatter)
logger.addHandler(error_handler)


class Product:
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
        logging.info(f"Продукт успешно инициализирован: '{self.name}'")

    def __str__(self) -> str:
        """Возвращает строковое представление продукта."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: Any) -> float:
        """Складывает общую стоимость двух продуктов ТОЛЬКО одинакового класса."""
        # Строгая проверка на строгое совпадение классов через type()
        if type(self) is not type(other):
            logging.error(f"Попытка сложения разных классов: {type(self).__name__} и {type(other).__name__}")
            raise TypeError("Складывать можно только товары одного и того же класса")

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
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color
        logging.info(f"Смартфон успешно инициализирован: '{self.model}'")


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
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color
        logging.info(f"Газонная трава успешно инициализирована: '{self.name}'")


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

    def add_product(self, product: Any) -> None:
        """Добавляет продукт в приватный список товаров категории с валидацией типа."""
        #  Проверка на принадлежность к классу Product или его наследникам через isinstance()
        if not isinstance(product, Product):
            logging.error(f"Попытка добавить некорректный объект в категорию: {type(product).__name__}")
            raise TypeError("В категорию можно добавлять только продукты или их наследников")

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
