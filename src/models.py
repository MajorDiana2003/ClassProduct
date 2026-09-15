import logging
from typing import Any, List, Optional

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class Product:
    """Класс для представления продукта."""

    name: str
    description: str
    #  Делаем атрибут цены приватным
    __price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        logging.info(f"Продукт успешно инициализирован: {self.name}")

    # Класс-метод для создания продукта из словаря с проверкой дубликатов
    @classmethod
    def new_product(
        cls, product_data: dict[str, Any], current_products: Optional[List["Product"]] = None
    ) -> "Product":
        """Фабричный метод для создания продукта из словаря."""
        name = product_data["name"]
        description = product_data["description"]
        price = product_data["price"]
        quantity = product_data["quantity"]

        #  если товар уже существует, объединяем его
        if current_products:
            for existing_product in current_products:
                if existing_product.name.lower() == name.lower():
                    existing_product.quantity += quantity
                    existing_product.price = max(existing_product.price, price)
                    logging.info(f"Обновлен существующий продукт-дубликат: {existing_product.name}")
                    return existing_product

        return cls(name, description, price, quantity)

    #  Геттер для приватной цены
    @property
    def price(self) -> float:
        """Геттер для получения цены продукта."""
        return self.__price

    #  Сеттер цены с валидацией и подтверждением понижения
    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для изменения цены."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        # Если цена понижается, запрашиваем подтверждение у пользователя
        if new_price < self.__price:
            user_answer = input(
                f"Вы уверены, что хотите понизить цену для {self.name} "
                f"с {self.__price} до {new_price} руб.? (y/n): "
            )
            if user_answer.lower() != "y":
                print("Действие отменено.")
                return

        self.__price = new_price


class Category:
    """Класс для представления категории продуктов."""

    category_count: int = 0
    product_count: int = 0

    name: str
    description: str
    #  Делаем атрибут списка товаров приватным
    __products: List[Product]

    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None) -> None:
        self.name = name
        self.description = description
        self.__products = []
        Category.category_count += 1

        if products is not None:
            for product in products:
                self.add_product(product)

        logging.info(f"Категория успешно инициализирована: {self.name}")

    # Публичный метод для добавления товара в приватный список
    def add_product(self, product: Product) -> None:
        """Добавляет продукт в приватный список товаров категории."""
        self.__products.append(product)
        Category.product_count += 1
        logging.info(f"В категорию '{self.name}' добавлен продукт: {product.name}")

    # Геттер возвращает продукты в виде отформатированных строк
    @property
    def products(self) -> str:
        """Возвращает строковое представление продуктов в категории."""
        result = []
        for product in self.__products:
            #  "Название продукта, X руб. Остаток: X шт."
            result.append(f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.")
        return "\n".join(result)
