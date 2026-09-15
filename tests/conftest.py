import pytest

from src.models import Category, Product


@pytest.fixture
def sample_product() -> Product:
    """Фикстура для создания тестового продукта."""
    return Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.00, 5)


@pytest.fixture
def sample_category(sample_product: Product) -> Category:
    """Фикстура для создания тестовой категории с продуктом."""
    # Сбрасываем счетчики перед тестом, чтобы они не накапливались в сессии pytest
    Category.category_count = 0
    Category.product_count = 0
    return Category("Смартфоны", "Смартфоны как средство коммуникации", [sample_product])
