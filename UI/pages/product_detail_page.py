import os
import warnings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from UI.data import (
    product_image_product_detail,
    product_title_product_detail,
    product_category_product_detail,
    product_price_product_detail,
    product_desc_title_product_detail,
    product_desc_text_product_detail,
    quantity_label_product_detail,
    quantity_decrease_product_detail,
    quantity_increase_product_detail,
    quantity_display_product_detail,
    add_to_cart_button_product_detail,
    free_shipping_text_product_detail,
    return_policy_text_product_detail,
    secure_payment_text_product_detail,
    CART_BADGE
)
from dotenv import load_dotenv

load_dotenv()


class ProductDetailPage(BasePage):

    def load_product(self, product_id: int):
        """Carga la URL del producto dinámicamente usando el product_id."""
        base_url = os.getenv("UI_PRODUCT_URL")
        self.visit(f"{base_url}{product_id}")

    def wait_for_product_loaded(self, product_id: int = 1):
        """Espera a que los elementos principales del producto estén visibles."""
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(product_title_product_detail(product_id))
        )
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(add_to_cart_button_product_detail(product_id))
        )

    def validate_product_elements(self, product_id: int = 1) -> bool:
        """Valida que todos los elementos del product detail estén visibles."""
        locators = [
            product_image_product_detail(product_id),
            product_title_product_detail(product_id),
            product_category_product_detail(product_id),
            product_price_product_detail(product_id),
            product_desc_title_product_detail(product_id),
            product_desc_text_product_detail(product_id),
            quantity_label_product_detail(product_id),
            quantity_decrease_product_detail(product_id),
            quantity_increase_product_detail(product_id),
            quantity_display_product_detail(product_id),
            add_to_cart_button_product_detail(product_id),
            free_shipping_text_product_detail(product_id),
            return_policy_text_product_detail(product_id),
            secure_payment_text_product_detail(product_id),
        ]
        for locator in locators:
            if not self.element_is_visible(locator):
                warnings.warn(f"⚠️ Elemento no visible: {locator}")
                return False
        return True

    # ======================
    # CARRITO
    # ======================
    def get_cart_badge_count(self) -> int:
        try:
            text = self.text_of_element(CART_BADGE)
            return int(text)
        except Exception:
            return 0

    def add_product_and_validate_badge(self, product_id: int = 1) -> bool:
        """Agrega el producto al carrito y valida que el badge aumente en 1."""
        before = self.get_cart_badge_count()
        self.click(add_to_cart_button_product_detail(product_id))
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: self.get_cart_badge_count() == before + 1
            )
            return True
        except Exception:
            warnings.warn(f"⚠️ Producto {product_id} NO se pudo agregar al carrito")
            return False

    # ======================
    # CANTIDAD
    # ======================
    def increment_quantity(self, product_id: int = 1):
        """Incrementa la cantidad del producto."""
        self.click(quantity_increase_product_detail(product_id))

    def decrement_quantity(self, product_id: int = 1):
        """Decrementa la cantidad del producto."""
        self.click(quantity_decrease_product_detail(product_id))

    def get_quantity(self, product_id: int = 1) -> int:
        """Retorna la cantidad actual mostrada en el PDP."""
        text = self.text_of_element(quantity_display_product_detail(product_id))
        return int(text)

    def get_product_name(self, product_id: int) -> str:
        """Devuelve el nombre del producto en el detalle (PDP)."""
        return self.text_of_element(product_title_product_detail(product_id))