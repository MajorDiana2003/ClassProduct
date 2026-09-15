from src.models import Category
from src.utils import load_products_from_json


def test_load_products_from_json() -> None:
    """Тест корректности загрузки данных и создания объектов из JSON."""
    # Полностью сбрасываем счетчики классов перед тестом
    Category.category_count = 0
    Category.product_count = 0

    # Загружаем данные из оригинального файла data/products.json
    categories = load_products_from_json("data/products.json")

    # 1. Проверяем, что загрузилось ровно 2 категории
    assert len(categories) == 2

    # 2. Проверяем первую категорию (Смартфоны) по её имени
    assert categories[0].name == "Смартфоны"

    # 3. Собираем имена продуктов из первой категории и приводим их к нижнему регистру
    product_names_lower = [product.name.lower() for product in categories[0].products]

    assert "samsung galaxy c23 ultra" in product_names_lower

    # 4. Проверяем вторую категорию (Телевизоры)
    assert categories[1].name == "Телевизоры"

    # 5. Проверяем, что итоговые счетчики сошлись: 2 категории и 4 уникальных продукта всего
    assert Category.category_count == 2
    assert Category.product_count == 4
