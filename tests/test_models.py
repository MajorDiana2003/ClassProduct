from src.models import Category, Product


def test_product_init(sample_product: Product) -> None:
    """Тест корректности инициализации объекта Product."""
    assert sample_product.name == "Samsung Galaxy S23 Ultra"
    assert sample_product.description == "256GB, Серый цвет, 200MP камера"
    assert sample_product.price == 180000.00
    assert sample_product.quantity == 5


def test_category_init(sample_category: Category, sample_product: Product) -> None:
    """Тест корректности инициализации объекта Category."""
    assert sample_category.name == "Смартфоны"
    assert sample_category.description == "Смартфоны как средство коммуникации"
    assert sample_category.products == [sample_product]


def test_category_counters(sample_category: Category) -> None:
    """Тест подсчета количества категорий и продуктов."""
    assert Category.category_count == 1
    assert Category.product_count == 1

    # Создаем еще одну категорию без товаров, проверяем изменение счетчика категорий
    Category("Телевизоры", "Современные телевизоры", [])
    assert Category.category_count == 2
    # Количество уникальных товаров не должно измениться
    assert Category.product_count == 1
