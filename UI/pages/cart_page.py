import os
import warnings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from UI.pages.base_page import BasePage
from UI.data import (
    CART_TITLE,
    CART_TITLE_EMPTY,
    CART_ORDER_SUMMARY_TITLE,
    CART_BUTTON_CHECKOUT,
    CART_BUTTON_CONTINUE_SHOPPING,
    CART_SUBTOTAL,
    CART_SHIPPING,
    CART_TAX,
    CART_TOTAL,
    CART_PRODUCT_CONTAINER_BY_NAME,
    CART_PRODUCT_QUANTITY,
    CART_PRODUCT_PRICE,
    CART_PRODUCT_INCREMENT,
    CART_PRODUCT_DECREMENT,
    CART_PRODUCT_REMOVE,
    OVERLAY,
    CHECKOUT_TITLE,
)
from dotenv import load_dotenv

load_dotenv()

UI_CHECKOUT_URL = os.getenv("UI_CHECKOUT_URL")

class CartPage(BasePage):

    def load_cart(self):
        base_url = os.getenv("UI_CART_URL")
        self.visit(base_url)

    def wait_for_cart_loaded(self, with_products: bool = True):
        if with_products:
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(CART_TITLE)
            )
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(CART_ORDER_SUMMARY_TITLE)
            )
        else:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(CART_TITLE_EMPTY)
            )

    # ======================
    # VALIDACIONES DE CARRITO
    # ======================
    def is_cart_empty(self) -> bool:
        return self.element_is_visible(CART_TITLE_EMPTY)

    def validate_order_summary(self) -> bool:
        locators = [CART_ORDER_SUMMARY_TITLE, CART_SUBTOTAL, CART_SHIPPING, CART_TAX, CART_TOTAL]
        for locator in locators:
            if not self.element_is_visible(locator):
                warnings.warn(f"⚠️ Elemento faltante en el resumen de orden: {locator}")
                return False
        return True

    # ======================
    # PRODUCTOS EN CARRITO
    # ======================

    def is_product_in_cart(self, product_name: str) -> bool:
        """Verifica que un producto esté presente en el carrito por su nombre."""
        return self.element_is_visible(CART_PRODUCT_CONTAINER_BY_NAME(product_name))

    def product_in_cart(self, product_name: str) -> bool:
        """Alias más legible para validación en tests."""
        return self.is_product_in_cart(product_name)

    def get_product_quantity(self, product_name: str) -> int:
        self.wait_for_overlay_to_disappear()
        locator = CART_PRODUCT_QUANTITY(product_name)
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(locator)
        )
        return int(element.text)

    def get_product_price(self, product_name: str) -> float:
        """
        Devuelve el precio del producto en el carrito como número (float),
        ignorando el símbolo $.
        """
        price_text = self.text_of_element(CART_PRODUCT_PRICE(product_name))

        # price_text puede ser "$\n22.99" o "$22.99"
        # Extraemos solo los números y el punto decimal
        import re
        match = re.search(r"\d+(\.\d+)?", price_text)
        if match:
            return float(match.group())
        raise ValueError(f"No se pudo extraer precio de: '{price_text}'")

    def increment_product_quantity(self, product_name: str):
        """Incrementa la cantidad de un producto, esperando overlay si existe."""
        self.wait_for_overlay_to_disappear()
        locator = CART_PRODUCT_INCREMENT(product_name)
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(locator))
        self.click(locator)

    def decrement_product_quantity(self, product_name: str):
        """Decrementa la cantidad de un producto, esperando overlay si existe."""
        self.wait_for_overlay_to_disappear()
        locator = CART_PRODUCT_DECREMENT(product_name)
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(locator))
        self.click(locator)

    def remove_product(self, product_name: str):
        self.click(CART_PRODUCT_REMOVE(product_name))

    def proceed_to_checkout(self):
        self.click(CART_BUTTON_CHECKOUT)

    def continue_shopping(self):
        self.click(CART_BUTTON_CONTINUE_SHOPPING)

    def proceed_to_checkout_and_validate(self, timeout=10):
        """Hace click en checkout y valida URL + título de Checkout."""
        self.wait_for_overlay_to_disappear()
        self.click(CART_BUTTON_CHECKOUT)
        WebDriverWait(self.driver, timeout).until(EC.url_to_be(UI_CHECKOUT_URL))
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(CHECKOUT_TITLE))
        return self.driver.current_url == UI_CHECKOUT_URL and self.driver.find_element(*CHECKOUT_TITLE).is_displayed()
