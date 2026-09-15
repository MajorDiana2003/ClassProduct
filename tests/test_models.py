import pytest

from src.models import Category, Product


def test_product_init(sample_product: Product) -> None:
    """Тест корректности инициализации объекта Product."""
    assert sample_product.name == "Samsung Galaxy S23 Ultra"
    assert sample_product.price == 180000.00
    assert sample_product.quantity == 5


def test_category_init(sample_category: Category) -> None:
    """Тест корректности инициализации объекта Category."""
    assert sample_category.name == "Смартфоны"
    # Проверяем, что продукт присутствует внутри строки геттера
    assert "Samsung Galaxy S23 Ultra" in sample_category.products


def test_category_products_string_getter(sample_category: Category) -> None:
    """Тест: проверка строкового формата геттера products."""
    expected_str = "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."
    assert sample_category.products == expected_str


def test_new_product_classmethod() -> None:
    """Тест: создание продукта через класс-метод из словаря."""
    data = {"name": "Iphone 15", "description": "512GB", "price": 210000.0, "quantity": 8}
    product = Product.new_product(data)
    assert product.name == "Iphone 15"
    assert product.price == 210000.0


def test_new_product_duplicate_addition() -> None:
    """Тест: сложение количества и выбор макс. цены для дубликатов."""
    p1 = Product("Iphone 15", "512GB", 1000.0, 5)
    products_list = [p1]

    new_data = {"name": "Iphone 15", "description": "Новый", "price": 1200.0, "quantity": 3}
    updated_p = Product.new_product(new_data, products_list)

    assert updated_p.quantity == 8  # 5 + 3
    assert updated_p.price == 1200.0  # max(1000, 1200)


def test_product_price_validation(sample_product: Product) -> None:
    """Тест: валидация изменения цены (отрицательные числа)."""
    # Некорректная цена не должна примениться
    sample_product.price = -100
    assert sample_product.price == 180000.00


def test_price_decrease_confirmed(sample_product: Product, monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест: подтверждение понижения цены пользователем (y)."""
    monkeypatch.setattr("builtins.input", lambda _: "y")
    sample_product.price = 150000.0
    assert sample_product.price == 150000.0


def test_price_decrease_cancelled(sample_product: Product, monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест: отмена понижения цены пользователем (n)."""
    monkeypatch.setattr("builtins.input", lambda _: "n")
    sample_product.price = 150000.0
    assert sample_product.price == 180000.0
