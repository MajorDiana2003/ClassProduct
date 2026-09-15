from src.models import Category
from src.utils import load_products_from_json


def test_load_products_from_json() -> None:
    """Тест корректности загрузки данных и создания объектов из JSON."""
    Category.category_count = 0
    Category.product_count = 0

    categories = load_products_from_json("data/products.json")

    assert len(categories) == 2
    assert categories[0].name == "Смартфоны"

    # Проверяем наличие продукта через новый строковый геттер .products
    assert "samsung galaxy c23 ultra" in categories[0].products.lower()

    assert categories[1].name == "Телевизоры"
    assert Category.category_count == 2
    assert Category.product_count == 4
