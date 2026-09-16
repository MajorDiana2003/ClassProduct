import pytest

from src.models import Category, CategoryIterator, LawnGrass, Order, Product, Smartphone


def test_product_init(sample_product: Product) -> None:
    """Тест инициализации и базовых атрибутов продукта."""
    assert sample_product.name == "Samsung Galaxy S23 Ultra"
    assert sample_product.description == "256GB, Серый цвет, 200MP камера"
    assert sample_product.price == 180000.00
    assert sample_product.quantity == 5


def test_category_init(sample_category: Category) -> None:
    """Тест инициализации и подсчета количества категорий и продуктов."""
    assert sample_category.name == "Смартфоны"
    assert sample_category.description == "Смартфоны как средство коммуникации"
    assert len(sample_category.products) == 1


def test_add_product_to_category(sample_category: Category) -> None:
    """Тест добавления продукта в существующую категорию."""
    new_product = Product("Xiaomi", "Бюджетный", 20000.0, 10)
    sample_category.add_product(new_product)
    assert len(sample_category.products) == 2


def test_price_setter(sample_product: Product, capsys: pytest.CaptureFixture[str]) -> None:
    """Тест изменения цены и отмены при некорректных значениях."""
    sample_product.price = -10.0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_product_str(sample_product: Product) -> None:
    """Тест магического метода __str__ для класса Product."""
    assert str(sample_product) == "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."


def test_category_str(sample_category: Category) -> None:
    """Тест магического метода __str__ для класса Category."""
    assert str(sample_category) == "Смартфоны, количество продуктов: 5 шт."


def test_product_addition(sample_product: Product) -> None:
    """Тест магического метода сложения __add__ для двух продуктов одинакового класса."""
    iphone = Product("Iphone 15", "512GB", 210000.0, 8)
    expected_total = 2580000.0
    assert sample_product + iphone == expected_total


def test_product_addition_type_error(sample_product: Product) -> None:
    """Тест, что сложение Product со сторонним типом данных вызывает TypeError."""
    with pytest.raises(TypeError):
        _ = sample_product + "Строка вместо объекта класса Product"


def test_category_iterator(sample_category: Category) -> None:
    """Тест работы класса-итератора CategoryIterator."""
    iterator = CategoryIterator(sample_category)
    iterated_products = [product for product in iterator]
    assert len(iterated_products) == 1
    assert iterated_products[0].name == "Samsung Galaxy S23 Ultra"


def test_smartphone_init() -> None:
    """Тест инициализации и атрибутов класса Smartphone."""
    phone = Smartphone("Iphone 15", "512GB", 210000.0, 8, 98.2, "15", 512, "Gray space")
    assert phone.name == "Iphone 15"
    assert phone.efficiency == 98.2


def test_lawngrass_init() -> None:
    """Тест инициализации и атрибутов класса LawnGrass."""
    grass = LawnGrass("Газонная трава", "Элитная", 500.0, 20, "Россия", "7 дней", "Зеленый")
    assert grass.name == "Газонная трава"
    assert grass.country == "Россия"


def test_add_products_different_classes() -> None:
    """Тест, что сложение разных классов (Smartphone + LawnGrass) вызывает TypeError."""
    phone = Smartphone("Iphone 15", "512GB", 210000.0, 8, 98.2, "15", 512, "Gray space")
    grass = LawnGrass("Газонная трава", "Элитная", 500.0, 20, "Россия", "7 дней", "Зеленый")

    with pytest.raises(TypeError):
        _ = phone + grass


def test_add_product_to_category_validation() -> None:
    """Тест, что добавление объекта, не являющегося Product, вызывает TypeError."""
    category = Category("Смартфоны", "Описание", [])
    with pytest.raises(TypeError):
        category.add_product("Просто строка вместо объекта")


def test_order_creation(sample_product: Product) -> None:
    """Тест создания заказа и расчета его стоимости."""
    order = Order(sample_product, 3)
    assert order.total_cost == 180000.0 * 3
    assert len(order.products) == 1


def test_order_invalid_product() -> None:
    """Тест вызова ошибки при передаче некорректного объекта в Заказ."""
    with pytest.raises(TypeError):
        _ = Order("Не продукт", 5)  # type: ignore


def test_mixin_repr(capsys: pytest.CaptureFixture[str]) -> None:
    """Тест, что миксин автоматически выводит repr объекта в консоль при создании."""
    _ = Product("Тест", "Описание", 100.0, 2)
    captured = capsys.readouterr()
    assert "Product('Тест', 'Описание', 100.0, 2)" in captured.out


def test_abstract_classes_cannot_be_instantiated() -> None:
    """Проверяем, что базовые классы защищены от прямого создания экземпляров."""
    from src.models import AbstractStorage, BaseProduct

    with pytest.raises(TypeError):
        BaseProduct()  # type: ignore

    with pytest.raises(TypeError):
        AbstractStorage()  # type: ignore
