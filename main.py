from src.models import Category, CategoryIterator, Product

if __name__ == "__main__":
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 310000.0, 14)

    print(str(product1))
    print(str(product2))
    print(str(product3))

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print(str(category1))

    # Вывод списка продуктов через геттер (в виде отформатированной строки)
    print("\nСписок продуктов в категории через геттер:")
    print(category1.products)

    # Проверка сложения двух продуктов
    print("\nПроверка сложения стоимостей:")
    print(f"Сумма product1 + product2: {product1 + product2} руб.")

    # --- Демонстрация работы дополнительного задания (итератора) ---
    print("\nПеребор продуктов категории поочередно через CategoryIterator:")
    iterator = CategoryIterator(category1)
    for product in iterator:
        print(f"Итератор вернул продукт: {product.name} (Остаток: {product.quantity} шт.)")
