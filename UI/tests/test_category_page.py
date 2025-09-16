import os
import pytest
import warnings
from UI.pages.category_page import CategoryPage


class TestCategoryPage:

    def test_men_clothes_category(self, driver):
        category = CategoryPage(driver)
        category.load_men_clothes()
        category.wait_for_men_clothes_page()

        # Validar URL
        assert driver.current_url == os.getenv("UI_MEN_CLOTHES_URL")

        # Validar que carguen productos o al menos la descripción
        category.wait_for_products_loaded()

        # Validar consistencia de productos y paginación
        assert category.validate_products_consistency()
        assert category.validate_pagination_consistency()

        # Obtener el total dinámico
        showing, total = category.get_products_count()
        assert total >= 0, "❌ El total de productos no puede ser negativo"

        # Validar elementos de cada producto visible en la página
        product_ids = category.get_product_ids_in_page()
        assert product_ids, "❌ No se encontraron productos visibles en la página"

        for pid in product_ids:
            assert category.validate_product_elements(pid), (
                f"❌ El producto con ID {pid} no tiene todos los elementos visibles"
            )

        # Validar agregar productos al carrito (warnings si falla)
        bugs = []
        for pid in product_ids:
            success = category.add_product_and_validate_badge(pid)
            if success:
                print(f"✅ Producto {pid} agregado al carrito")
            else:
                warnings.warn(f"⚠️ Producto {pid} NO se pudo agregar al carrito")
                bugs.append(pid)

        if bugs:
            warnings.warn(f"⚠️ Total de productos que no se agregaron al carrito: {bugs}")


    def test_women_clothes_category(self, driver):
        category = CategoryPage(driver)
        category.load_women_clothes()
        category.wait_for_women_clothes_page()

        assert driver.current_url == os.getenv("UI_WOMEN_CLOTHES_URL")
        category.wait_for_products_loaded()
        assert category.validate_products_consistency()
        assert category.validate_pagination_consistency()

        showing, total = category.get_products_count()
        assert total >= 0, "❌ El total de productos no puede ser negativo"

        product_ids = category.get_product_ids_in_page()
        assert product_ids, "❌ No se encontraron productos visibles en la página"

        for pid in product_ids:
            assert category.validate_product_elements(pid), (
                f"❌ Women Clothes - producto {pid} no tiene todos los elementos visibles"
            )

        bugs = []
        for pid in product_ids:
            success = category.add_product_and_validate_badge(pid)
            if success:
                print(f"✅ Producto {pid} agregado al carrito")
            else:
                warnings.warn(f"⚠️ Producto {pid} NO se pudo agregar al carrito")
                bugs.append(pid)

        if bugs:
            warnings.warn(f"⚠️ Total de productos que no se agregaron al carrito: {bugs}")


    def test_electronics_category(self, driver):
        category = CategoryPage(driver)
        category.load_electronics()
        category.wait_for_electronics_page()

        assert driver.current_url == os.getenv("UI_ELECTRONICS_URL")
        category.wait_for_products_loaded()
        assert category.validate_products_consistency()
        assert category.validate_pagination_consistency()

        showing, total = category.get_products_count()
        assert total >= 0, "❌ El total de productos no puede ser negativo"

        product_ids = category.get_product_ids_in_page()
        assert product_ids, "❌ No se encontraron productos visibles en la página"

        for pid in product_ids:
            assert category.validate_product_elements(pid), (
                f"❌ Electronics - producto {pid} no tiene todos los elementos visibles"
            )

        bugs = []
        for pid in product_ids:
            success = category.add_product_and_validate_badge(pid)
            if success:
                print(f"✅ Producto {pid} agregado al carrito")
            else:
                warnings.warn(f"⚠️ Producto {pid} NO se pudo agregar al carrito")
                bugs.append(pid)

        if bugs:
            warnings.warn(f"⚠️ Total de productos que no se agregaron al carrito: {bugs}")


    def test_books_category(self, driver):
        category = CategoryPage(driver)
        category.load_books()
        category.wait_for_books_page()

        assert driver.current_url == os.getenv("UI_BOOKS_URL")
        category.wait_for_products_loaded()
        assert category.validate_products_consistency()
        assert category.validate_pagination_consistency()

        showing, total = category.get_products_count()
        assert total >= 0, "❌ El total de productos no puede ser negativo"

        product_ids = category.get_product_ids_in_page()
        assert product_ids, "❌ No se encontraron productos visibles en la página"

        for pid in product_ids:
            assert category.validate_product_elements(pid), (
                f"❌ Books - producto {pid} no tiene todos los elementos visibles"
            )

        bugs = []
        for pid in product_ids:
            success = category.add_product_and_validate_badge(pid)
            if success:
                print(f"✅ Producto {pid} agregado al carrito")
            else:
                warnings.warn(f"⚠️ Producto {pid} NO se pudo agregar al carrito")
                bugs.append(pid)

        if bugs:
            warnings.warn(f"⚠️ Total de productos que no se agregaron al carrito: {bugs}")


    def test_groceries_category(self, driver):
        category = CategoryPage(driver)
        category.load_groceries()
        category.wait_for_groceries_page()

        assert driver.current_url == os.getenv("UI_GROCERIES_URL")
        category.wait_for_products_loaded()
        assert category.validate_products_consistency()
        assert category.validate_pagination_consistency()

        showing, total = category.get_products_count()
        assert total >= 0, "❌ El total de productos no puede ser negativo"

        product_ids = category.get_product_ids_in_page()
        assert product_ids, "❌ No se encontraron productos visibles en la página"

        for pid in product_ids:
            assert category.validate_product_elements(pid), (
                f"❌ Groceries - producto {pid} no tiene todos los elementos visibles"
            )

        bugs = []
        for pid in product_ids:
            success = category.add_product_and_validate_badge(pid)
            if success:
                print(f"✅ Producto {pid} agregado al carrito")
            else:
                warnings.warn(f"⚠️ Producto {pid} NO se pudo agregar al carrito")
                bugs.append(pid)

        if bugs:
            warnings.warn(f"⚠️ Total de productos que no se agregaron al carrito: {bugs}")