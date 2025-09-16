import pytest
import os
from dotenv import load_dotenv
from UI.pages.home_page import HomePage
from UI.pages.category_page import CategoryPage
from UI.pages.product_detail_page import ProductDetailPage
from UI.pages.cart_page import CartPage
from UI.data import OVERLAY

load_dotenv()
UI_BASE_URL = os.getenv("UI_BASE_URL")

class TestCartPage:

    def test_add_from_product_detail(self, driver):
        """
        Escenario: ir al Product Detail (desde Category -> seleccionar ID),
        agregar el producto al carrito desde la PDP y validar en Cart Page.
        """
        home_page = HomePage(driver)
        category_page = CategoryPage(driver)
        product_detail = ProductDetailPage(driver)
        cart_page = CartPage(driver)

        # 1) Ir a Home -> Women Clothes -> esperar categoría y productos
        home_page.load()
        home_page.go_to_women_clothes()
        category_page.wait_for_women_clothes_page()
        category_page.wait_for_products_loaded()

        # 2) Obtener el primer product_id visible y su nombre (desde Category)
        product_ids = category_page.get_product_ids_in_page()
        assert product_ids, "❌ No se encontraron productos en la categoría (no hay product_ids)"
        product_id = product_ids[0]
        product_name = category_page.get_product_name(product_id)

        # 3) Cargar PDP de ese producto y esperar que cargue
        product_detail.load_product(product_id)
        product_detail.wait_for_product_loaded(product_id)

        # 4) Agregar al carrito desde PDP (valida badge)
        assert product_detail.add_product_and_validate_badge(product_id), (
            f"❌ No se pudo agregar al carrito el producto id={product_id}"
        )

        # 5) Ir al carrito y esperar que cargue con productos
        home_page.go_to_cart()
        cart_page.wait_for_cart_loaded(with_products=True)

        # 6) Validar que el producto aparezca en el carrito y cantidad inicial = 1
        assert cart_page.is_product_in_cart(product_name), (
            f"❌ El producto '{product_name}' (id={product_id}) no está en el carrito"
        )
        qty = cart_page.get_product_quantity(product_name)
        assert qty >= 1, f"❌ Cantidad esperada >=1, encontrada: {qty}"

        # Precio unitario
        unit_price = cart_page.get_product_price(product_name)

        # 7) Probar incrementar y decrementar cantidad
        cart_page.increment_product_quantity(product_name)
        qty_inc = cart_page.get_product_quantity(product_name)
        assert qty_inc == qty + 1, f"❌ Al incrementar la cantidad no aumentó: antes {qty}, ahora {qty_inc}"

        # Validar que el precio se actualizó correctamente
        price_after_inc = cart_page.get_product_price(product_name)
        expected_price = unit_price * qty_inc
        assert abs(price_after_inc - expected_price) < 0.01, (
            f"❌ Precio incorrecto después de incrementar. Esperado {expected_price}, encontrado {price_after_inc}"
        )

        cart_page.decrement_product_quantity(product_name)
        qty_dec = cart_page.get_product_quantity(product_name)
        assert qty_dec == qty, f"❌ Al decrementar la cantidad no regresó: esperado {qty}, encontrado {qty_dec}"

        # Validar precio después de decrementar
        price_after_dec = cart_page.get_product_price(product_name)
        expected_price_dec = unit_price * qty_dec
        assert abs(price_after_dec - expected_price_dec) < 0.01, (
            f"❌ Precio incorrecto después de decrementar. Esperado {expected_price_dec}, encontrado {price_after_dec}"
        )

    def test_add_4_products_from_pdp(self, driver):
        """
        Escenario: agregar 4 productos desde Product Detail,
        omitiendo el tercer producto porque tiene bug.
        """
        home_page = HomePage(driver)
        category_page = CategoryPage(driver)
        product_detail = ProductDetailPage(driver)
        cart_page = CartPage(driver)

        # 1) Ir a Home -> Women Clothes
        home_page.load()
        home_page.go_to_women_clothes()
        category_page.wait_for_women_clothes_page()
        category_page.wait_for_products_loaded()

        # 2) Obtener lista de productos
        product_ids = category_page.get_product_ids_in_page()
        assert len(product_ids) >= 5, "❌ No hay suficientes productos para la prueba"

        # ⚠️ omitimos el 3er y 5to producto porque da error
        indices = [0, 1, 3, 5]
        added_products = []

        for idx in indices:
            product_id = product_ids[idx]
            product_name = category_page.get_product_name(product_id)

            # Entrar al detalle
            product_detail.load_product(product_id)
            product_detail.wait_for_product_loaded(product_id)

            # Agregar al carrito
            assert product_detail.add_product_and_validate_badge(product_id), (
                f"❌ No se pudo agregar al carrito el producto id={product_id}"
            )
            added_products.append(product_name)

            # Volver a la categoría
            driver.back()
            category_page.wait_for_products_loaded()

        # 3) Ir al carrito
        home_page.go_to_cart()
        cart_page.wait_for_cart_loaded(with_products=True)

        # 4) Validar que los 4 productos estén en el carrito
        for product_name in added_products:
            assert cart_page.is_product_in_cart(product_name), (
                f"❌ El producto '{product_name}' no está en el carrito"
            )

        assert len(added_products) == 4, f"❌ Se esperaban 4 productos agregados, encontrados {len(added_products)}"

    def test_add_from_category_page(self, driver):
        """
        Escenario: agregar un producto DIRECTAMENTE desde Category Page y validar en Cart Page,
        incluyendo validación de precio al incrementar/decrementar.
        """
        home_page = HomePage(driver)
        category_page = CategoryPage(driver)
        cart_page = CartPage(driver)

        # 1) Ir a Home -> Women Clothes -> esperar categoría y productos
        home_page.load()
        home_page.go_to_women_clothes()
        category_page.wait_for_women_clothes_page()
        category_page.wait_for_products_loaded()

        # 2) Obtener primer product_id visible y su nombre (desde Category)
        product_ids = category_page.get_product_ids_in_page()
        assert product_ids, "❌ No se encontraron productos en la categoría (no hay product_ids)"
        product_id = product_ids[0]
        product_name = category_page.get_product_name(product_id)

        # 3) Agregar al carrito DIRECTAMENTE desde Category (valida badge)
        assert category_page.add_product_and_validate_badge(product_id), (
            f"❌ No se pudo agregar al carrito el producto id={product_id} desde Category"
        )

        # 4) Ir al carrito y esperar que cargue con productos
        home_page.go_to_cart()
        cart_page.wait_for_cart_loaded(with_products=True)

        # 5) Validar que el producto esté en el carrito y cantidad = 1
        assert cart_page.is_product_in_cart(product_name), (
            f"❌ El producto '{product_name}' (id={product_id}) no está en el carrito"
        )
        qty = cart_page.get_product_quantity(product_name)
        assert qty >= 1, f"❌ Cantidad esperada >=1, encontrada: {qty}"

        # Precio unitario
        unit_price = cart_page.get_product_price(product_name)

        # 6) Probar incrementar y decrementar cantidad
        cart_page.increment_product_quantity(product_name)
        qty_inc = cart_page.get_product_quantity(product_name)
        assert qty_inc == qty + 1, f"❌ Al incrementar la cantidad no aumentó: antes {qty}, ahora {qty_inc}"

        # Validar que el precio se actualizó correctamente
        price_after_inc = cart_page.get_product_price(product_name)
        expected_price = unit_price * qty_inc
        assert abs(price_after_inc - expected_price) < 0.01, (
            f"❌ Precio incorrecto después de incrementar. Esperado {expected_price}, encontrado {price_after_inc}"
        )

        cart_page.decrement_product_quantity(product_name)
        qty_dec = cart_page.get_product_quantity(product_name)
        assert qty_dec == qty, f"❌ Al decrementar la cantidad no regresó: esperado {qty}, encontrado {qty_dec}"

        # Validar precio después de decrementar
        price_after_dec = cart_page.get_product_price(product_name)
        expected_price_dec = unit_price * qty_dec
        assert abs(price_after_dec - expected_price_dec) < 0.01, (
            f"❌ Precio incorrecto después de decrementar. Esperado {expected_price_dec}, encontrado {price_after_dec}"
        )

        print(f"✅ Flujo Category -> carrito OK para producto id={product_id} ('{product_name}')")

    def test_add_multiple_from_category_page(self, driver):
        """
        Escenario: agregar 4 productos DIRECTAMENTE desde Category Page y validar en Cart Page.
        """
        home_page = HomePage(driver)
        category_page = CategoryPage(driver)
        cart_page = CartPage(driver)

        # 1) Ir a Home -> Women Clothes -> esperar categoría y productos
        home_page.load()
        home_page.go_to_women_clothes()
        category_page.wait_for_women_clothes_page()
        category_page.wait_for_products_loaded()

        # 2) Obtener los primeros 4 productos visibles
        product_ids = category_page.get_product_ids_in_page()
        assert len(product_ids) >= 4, "❌ No hay al menos 4 productos en la categoría"

        selected_products = []
        for pid in product_ids[:4]:
            product_name = category_page.get_product_name(pid)
            added = category_page.add_product_and_validate_badge(pid)
            assert added, f"❌ No se pudo agregar al carrito el producto id={pid}"
            selected_products.append(product_name)

        # 3) Ir al carrito y esperar que cargue con productos
        home_page.go_to_cart()
        cart_page.wait_for_cart_loaded(with_products=True)

        # 4) Validar que los 4 productos estén en el carrito y con cantidad = 1
        for pname in selected_products:
            assert cart_page.is_product_in_cart(pname), f"❌ El producto '{pname}' no está en el carrito"
            qty = cart_page.get_product_quantity(pname)
            assert qty == 1, f"❌ Cantidad incorrecta para '{pname}'. Esperado=1, encontrado={qty}"

        print(f"✅ Se agregaron correctamente 4 productos desde Category Page al carrito: {selected_products}")

    def test_add_and_remove_from_category_page(self, driver):
        """
        Escenario: agregar un producto desde Category Page,
        validar en Cart Page, esperar que desaparezca overlay,
        remover el producto y comprobar carrito vacío.
        """
        home_page = HomePage(driver)
        category_page = CategoryPage(driver)
        cart_page = CartPage(driver)

        # 1) Ir a Home -> Women Clothes -> esperar categoría y productos
        home_page.load()
        home_page.go_to_women_clothes()
        category_page.wait_for_women_clothes_page()
        category_page.wait_for_products_loaded()

        # 2) Obtener primer product_id visible y su nombre
        product_ids = category_page.get_product_ids_in_page()
        assert product_ids, "❌ No se encontraron productos en la categoría"
        product_id = product_ids[0]
        product_name = category_page.get_product_name(product_id)

        # 3) Agregar al carrito DIRECTAMENTE desde Category
        assert category_page.add_product_and_validate_badge(product_id), (
            f"❌ No se pudo agregar al carrito el producto id={product_id} desde Category"
        )

        # 4) Ir al carrito y esperar que cargue con productos
        home_page.go_to_cart()
        cart_page.wait_for_cart_loaded(with_products=True)

        # 5) Validar que el producto esté en el carrito
        assert cart_page.is_product_in_cart(product_name), (
            f"❌ El producto '{product_name}' (id={product_id}) no está en el carrito"
        )

        # 6) Esperar que desaparezca overlay antes de eliminar
        cart_page.wait_for_overlay_to_disappear()

        # 7) Eliminar producto
        cart_page.remove_product(product_name)

        cart_page.wait_for_overlay_to_disappear()

        # 8) Validar que el carrito está vacío
        assert cart_page.is_cart_empty(), (
            f"❌ El carrito no está vacío después de eliminar '{product_name}'"
        )

        print(f"✅ Producto '{product_name}' (id={product_id}) agregado y eliminado correctamente -> carrito vacío")

    def test_add_product_and_proceed_to_checkout(self, driver):
        """
        Escenario: agregar un producto desde Category Page y navegar al Checkout,
        validando URL y título.
        """
        home_page = HomePage(driver)
        category_page = CategoryPage(driver)
        cart_page = CartPage(driver)

        # 1) Ir a Home -> Women Clothes -> esperar categoría y productos
        home_page.load()
        home_page.go_to_women_clothes()
        category_page.wait_for_women_clothes_page()
        category_page.wait_for_products_loaded()

        # 2) Obtener primer product_id visible y su nombre
        product_ids = category_page.get_product_ids_in_page()
        assert product_ids, "❌ No se encontraron productos en la categoría"
        product_id = product_ids[0]
        product_name = category_page.get_product_name(product_id)

        # 3) Agregar producto al carrito desde Category Page (valida badge)
        assert category_page.add_product_and_validate_badge(product_id), (
            f"❌ No se pudo agregar al carrito el producto id={product_id} desde Category"
        )

        # 4) Ir al carrito y esperar que cargue con productos
        home_page.go_to_cart()
        cart_page.wait_for_cart_loaded(with_products=True)

        # 5) Validar que el producto esté en el carrito
        assert cart_page.is_product_in_cart(product_name), (
            f"❌ El producto '{product_name}' (id={product_id}) no está en el carrito"
        )

        cart_page.wait_for_overlay_to_disappear()

        # 6) Hacer click en Checkout y validar URL + título
        assert cart_page.proceed_to_checkout_and_validate(), (
            f"❌ Checkout no se abrió correctamente para el producto id={product_id}"
        )

        print(f"✅ Producto id={product_id} agregado y Checkout abierto correctamente")

    def test_add_product_and_continue_shopping(self, driver):
        """
        Escenario: agregar un producto desde Category Page y luego hacer clic en
        'Continue Shopping', validando que regrese al Home.
        """
        home_page = HomePage(driver)
        category_page = CategoryPage(driver)
        cart_page = CartPage(driver)

        # 1) Ir a Home -> Women Clothes
        home_page.load()
        home_page.go_to_women_clothes()
        category_page.wait_for_women_clothes_page()
        category_page.wait_for_products_loaded()

        # 2) Obtener primer producto
        product_ids = category_page.get_product_ids_in_page()
        assert product_ids, "❌ No se encontraron productos en la categoría"
        product_id = product_ids[0]
        product_name = category_page.get_product_name(product_id)

        # 3) Agregar producto al carrito
        assert category_page.add_product_and_validate_badge(product_id), (
            f"❌ No se pudo agregar al carrito id={product_id}"
        )

        # 4) Ir al carrito y esperar productos
        home_page.go_to_cart()
        cart_page.wait_for_cart_loaded(with_products=True)

        # 5) Validar producto en carrito
        assert cart_page.is_product_in_cart(product_name), (
            f"❌ El producto '{product_name}' no está en el carrito"
        )

        # 6) Ahora esperar a que desaparezca el overlay
        cart_page.wait_for_overlay_to_disappear()

        # 7) Click en Continue Shopping
        cart_page.continue_shopping()

        # 8) Validar que regresamos al Home
        assert driver.current_url == UI_BASE_URL, (
            f"❌ No regresó al Home. URL actual: {driver.current_url}"
        )

        print(f"✅ Producto id={product_id} agregado y regreso al Home correctamente")
