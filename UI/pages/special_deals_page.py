import os
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from UI.data import CATEGORY_DESCRIPTION
from dotenv import load_dotenv

load_dotenv()

class SpecialDealsPage(BasePage):

    def load_page(self):
        """Carga la página de Special Deals."""
        self.visit(os.getenv("UI_SPECIAL_DEALS_URL"))

    def wait_for_page_loaded(self):
        """Espera a que la página cargue su descripción."""
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(CATEGORY_DESCRIPTION)
        )

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
        Valida consistencia de productos (aunque sea 0).
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
        Valida consistencia de paginación.
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