from ..data import (
    CHECKOUT_TITLE,
    CHECKOUT_COMPLETE_TITLE,
    CHECKOUT_COMPLETE_INPUT_FIRST_NAME,
    CHECKOUT_COMPLETE_INPUT_LAST_NAME,
    CHECKOUT_COMPLETE_INPUT_EMAIL,
    CHECKOUT_COMPLETE_INPUT_PHONE,
    CHECKOUT_COMPLETE_INPUT_ADDRESS,
    CHECKOUT_COMPLETE_INPUT_CITY,
    CHECKOUT_COMPLETE_INPUT_ZIP_CODE,
    CHECKOUT_COMPLETE_INPUT_COUNTRY,
    CHECKOUT_COMPLETE_BUTTON_PLACE_ORDER,
    CHECKOUT_COMPLETE_EXPECTED_LABELS,
)
from .base_page import BasePage
from selenium.common.exceptions import NoAlertPresentException


class CheckoutPage(BasePage):

    def is_loaded(self) -> bool:
        """Valida que la página de Checkout se cargó correctamente."""
        return self.element_is_visible(CHECKOUT_TITLE)

    def is_customer_info_loaded(self) -> bool:
        """Valida que la sección Customer Info esté visible."""
        return self.element_is_visible(CHECKOUT_COMPLETE_TITLE)

    def validate_field_labels(self) -> bool:
        """Valida que los labels de los fields coincidan con lo esperado."""
        for locator, expected_text in CHECKOUT_COMPLETE_EXPECTED_LABELS.items():
            label_text = self.text_of_element(locator)
            if label_text.strip() != expected_text:
                print(f"❌ Label incorrecto en {locator}: '{label_text}' en lugar de '{expected_text}'")
                return False
        return True

    def fill_checkout_form(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        address: str,
        city: str,
        zip_code: str,
        country: str,
    ):
        """Llena todos los campos obligatorios del formulario de Checkout."""
        self.type(CHECKOUT_COMPLETE_INPUT_FIRST_NAME, first_name)
        self.type(CHECKOUT_COMPLETE_INPUT_LAST_NAME, last_name)
        self.type(CHECKOUT_COMPLETE_INPUT_EMAIL, email)
        self.type(CHECKOUT_COMPLETE_INPUT_PHONE, phone)
        self.type(CHECKOUT_COMPLETE_INPUT_ADDRESS, address)
        self.type(CHECKOUT_COMPLETE_INPUT_CITY, city)
        self.type(CHECKOUT_COMPLETE_INPUT_ZIP_CODE, zip_code)
        self.type(CHECKOUT_COMPLETE_INPUT_COUNTRY, country)

    def place_order(self):
        """Hace click en 'Place Order'."""
        self.wait_for_overlay_to_disappear()
        self.click(CHECKOUT_COMPLETE_BUTTON_PLACE_ORDER)

    def handle_alert_and_get_text(self) -> str | None:
        """Si hay alerta, devuelve el texto y la acepta; si no, None."""
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            return alert_text
        except NoAlertPresentException:
            return None