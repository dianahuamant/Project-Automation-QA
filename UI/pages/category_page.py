import os
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from UI.data import (
    CATEGORY_TITLE_MEN_CLOTHES,
    CATEGORY_TITLE_WOMEN_CLOTHES,
    CATEGORY_TITLE_ELECTRONICS,
    CATEGORY_TITLE_BOOKS,
    CATEGORY_TITLE_GROCERIES,
    CATEGORY_DESCRIPTION,
    CATEGORY_PRODUCT_CONTAINER,
    CART_BADGE,
    product_image,
    product_name,
    product_desc,
    product_price,
    product_view_details,
    product_add_to_cart
)
from dotenv import load_dotenv
from UI.pages.cart_page import CartPage

load_dotenv()


class CategoryPage(BasePage):

    # ======================
    # LOADERS POR CATEGORÍA
    # ======================
    def load_men_clothes(self):
        self.visit(os.getenv("UI_MEN_CLOTHES_URL"))

    def load_women_clothes(self):
        self.visit(os.getenv("UI_WOMEN_CLOTHES_URL"))

    def load_electronics(self):
        self.visit(os.getenv("UI_ELECTRONICS_URL"))

    def load_books(self):
        self.visit(os.getenv("UI_BOOKS_URL"))

    def load_groceries(self):
        self.visit(os.getenv("UI_GROCERIES_URL"))

    # ======================
    # WAITS
    # ======================
    def wait_for_men_clothes_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(CATEGORY_TITLE_MEN_CLOTHES)
        )

    def wait_for_women_clothes_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(CATEGORY_TITLE_WOMEN_CLOTHES)
        )

    def wait_for_electronics_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(CATEGORY_TITLE_ELECTRONICS)
        )

    def wait_for_books_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(CATEGORY_TITLE_BOOKS)
        )

    def wait_for_groceries_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(CATEGORY_TITLE_GROCERIES)
        )

    # ======================
    # VALIDACIONES DE PÁGINA
    # ======================
    def wait_for_products_loaded(self):
        """Valida que la categoría haya cargado (aunque pueda tener 0 productos)."""
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(CATEGORY_DESCRIPTION)
        )
        # Solo esperar productos si efectivamente hay mostrados > 0
        showing, total = self.get_products_count()
        if showing > 0:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(CATEGORY_PRODUCT_CONTAINER)
            )

    # ---------- Métodos dinámicos ----------
    def get_products_count(self) -> tuple[int, int]:
        """
        Devuelve (mostrados, total) a partir de 'Showing X of Y products'.
        """
        text = self.text_of_element(CATEGORY_DESCRIPTION)
        match = re.search(r"Showing (\d+) of (\d+) products", text)
        if match:
            showing = int(match.group(1))
            total = int(match.group(2))
            return showing, total
        raise ValueError(f"No se pudo leer los productos en: {text}")

    def get_pagination_info(self) -> tuple[int, int]:
        """
        Devuelve (pagina_actual, total_paginas) a partir de '(Page Z of W)'.
        """
        text = self.text_of_element(CATEGORY_DESCRIPTION)
        match = re.search(r"Page (\d+) of (\d+)", text)
        if match:
            current_page = int(match.group(1))
            total_pages = int(match.group(2))
            return current_page, total_pages
        raise ValueError(f"No se pudo leer la paginación en: {text}")

    def validate_products_consistency(self) -> bool:
        """
        Valida que la cantidad mostrada no sea mayor al total
        y que nunca aparezca 'X of 0' con X > 0.
        """
        showing, total = self.get_products_count()
        if total == 0 and showing > 0:
            raise AssertionError("❌ Bug: Se muestran productos pero el total es 0")
        if showing > total:
            raise AssertionError(
                f"❌ Bug: Productos mostrados ({showing}) mayor al total ({total})"
            )
        return True

    def validate_pagination_consistency(self) -> bool:
        """
        Valida que la paginación tenga sentido.
        """
        showing, total = self.get_products_count()
        current_page, total_pages = self.get_pagination_info()

        if total == 0:
            if current_page != 0 or total_pages != 0:
                raise AssertionError(
                    f"❌ Bug: Si no hay productos, la paginación debería ser Page 0 of 0. "
                    f"Actual: Page {current_page} of {total_pages}"
                )
        else:
            if current_page < 1 or current_page > total_pages:
                raise AssertionError(
                    f"❌ Bug: Página actual ({current_page}) fuera de rango (1..{total_pages})"
                )
            if total_pages < 1:
                raise AssertionError(
                    f"❌ Bug: Total de páginas inválido ({total_pages})"
                )
        return True

    def get_product_ids_in_page(self) -> list[int]:
        """
        Devuelve todos los IDs de productos visibles en la página actual.
        Se basa en el atributo id="product-content-<n>".
        """
        elements = self.driver.find_elements(*CATEGORY_PRODUCT_CONTAINER)
        product_ids = []
        for el in elements:
            attr_id = el.get_attribute("id")  # ejemplo: product-content-11
            match = re.search(r"product-content-(\d+)", attr_id)
            if match:
                product_ids.append(int(match.group(1)))
        return product_ids

    def validate_product_elements(self, product_id: int) -> bool:
        """
        Valida que el producto con cierto ID tenga:
        imagen, nombre, descripción, precio, view details y carrito.
        """
        product_locators = [
            product_image(product_id),
            product_name(product_id),
            product_desc(product_id),
            product_price(product_id),
            product_view_details(product_id),
            product_add_to_cart(product_id),
        ]

        for locator in product_locators:
            if not self.element_is_visible(locator):
                return False
        return True

    # ======================
    # CARRITO
    # ======================
    def get_cart_badge_count(self) -> int:
        """Devuelve el número actual de productos en el carrito (0 si no existe badge)."""
        try:
            text = self.text_of_element(CART_BADGE)
            return int(text)
        except Exception:
            return 0

    def add_product_by_id(self, product_id: int):
        """Hace clic en el ícono del carrito para agregar un producto."""
        locator = product_add_to_cart(product_id)
        self.click(locator)

    def add_product_and_validate_badge(self, product_id: int) -> bool:
        """
        Intenta agregar el producto al carrito y valida que el badge aumente en 1.
        Devuelve True si se agregó correctamente, False si no.
        """
        before = self.get_cart_badge_count()
        self.wait_for_overlay_to_disappear()
        self.click(product_add_to_cart(product_id))

        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: self.get_cart_badge_count() == before + 1
            )
            return True
        except Exception:
            return False

    #Convierte id a name
    def get_product_name(self, product_id: int) -> str:
        """Devuelve el nombre del producto en la página de categoría."""
        return self.text_of_element(product_name(product_id))