import pytest

from src.models import Category, CategoryIterator, LawnGrass, Product, Smartphone


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


def test_product_str(sample_product: Product) -> None:
    """Тест магического метода __str__ для класса Product."""
    assert str(sample_product) == "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."


def test_category_str(sample_category: Category) -> None:
    """Тест магического метода __str__ для класса Category."""
    assert str(sample_category) == "Смартфоны, количество продуктов: 5 шт."


def test_product_addition(sample_product: Product) -> None:
    """Тест магического метода сложения __add__ для двух продуктов."""
    # Создаем второй продукт для теста сложения
    iphone = Product("Iphone 15", "512GB", 210000.0, 8)

    # Расчет стоимости на складе:
    # (180000.0 * 5) + (210000.0 * 8) = 900000.0 + 1680000.0 = 2580000.0
    expected_total = 2580000.0
    assert sample_product + iphone == expected_total


def test_product_addition_type_error(sample_product: Product) -> None:
    """Тест, что сложение Product со сторонним типом данных вызывает TypeError."""
    with pytest.raises(TypeError):
        _ = sample_product + "Строка вместо объекта класса Product"


def test_category_iterator(sample_category: Category) -> None:
    """Тест работы класса-итератора CategoryIterator."""

    iterator = CategoryIterator(sample_category)

    # Собираем продукты, перебирая созданный итератор в цикле
    iterated_products = [product for product in iterator]

    # Проверяем, что итератор выдал ровно 1 продукт и это наш Samsung
    assert len(iterated_products) == 1
    assert iterated_products[0].name == "Samsung Galaxy S23 Ultra"


def test_smartphone_init() -> None:
    """Тест инициализации и атрибутов класса Smartphone."""
    phone = Smartphone("Iphone 15", "512GB", 210000.0, 8, 98.2, "15", 512, "Gray space")
    assert phone.name == "Iphone 15"
    assert phone.efficiency == 98.2
    assert phone.memory == 512


def test_lawngrass_init() -> None:
    """Тест инициализации и атрибутов класса LawnGrass."""
    grass = LawnGrass("Газонная трава", "Элитная", 500.0, 20, "Россия", "7 дней", "Зеленый")
    assert grass.name == "Газонная трава"
    assert grass.country == "Россия"
    assert grass.germination_period == "7 дней"


def test_add_products_different_classes() -> None:
    """Тест, что сложение разных классов (Smartphone + LawnGrass) вызывает TypeError."""
    phone = Smartphone("Iphone 15", "512GB", 210000.0, 8, 98.2, "15", 512, "Gray space")
    grass = LawnGrass("Газонная трава", "Элитная", 500.0, 20, "Россия", "7 дней", "Зеленый")

    with pytest.raises(TypeError):
        _ = phone + grass


def test_add_product_to_category_validation() -> None:
    """Тест, что добавление объекта, не являющегося Product или его наследником, вызывает TypeError."""
    category = Category("Смартфоны", "Описание", [])
    with pytest.raises(TypeError):
        category.add_product("Просто строка вместо объекта")
