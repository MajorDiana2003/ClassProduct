import pytest

from src.models import Category, Product


@pytest.fixture
def sample_product() -> Product:
    """Фикстура для создания тестового продукта."""
    return Product(
        name="Samsung Galaxy S23 Ultra",
        description="256GB, Серый цвет, 200MP камера",
        price=180000.00,
        quantity=5,
    )


@pytest.fixture
def sample_category(sample_product: Product) -> Category:
    """Фикстура для создания тестовой категории со списком продуктов."""
    # Сбрасываем счетчики перед тестом, чтобы они не накапливались в сессии pytest
    Category.category_count = 0
    Category.product_count = 0
    return Category(
        name="Смартфоны",
        description="Смартфоны как средство коммуникации",
        products=[sample_product],
    )
