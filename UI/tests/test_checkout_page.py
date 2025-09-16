import os
import pytest
from UI.utils.faker_data import random_first_name, random_last_name, random_email, random_zip_code,random_city, random_address, random_phone, random_country
from UI.pages.home_page import HomePage
from UI.pages.category_page import CategoryPage
from UI.pages.cart_page import CartPage
from UI.pages.checkout_page import CheckoutPage

# -----------------------------------
# Casos de obligatoriedad en Checkout
# -----------------------------------
checkout_cases = [
    # Casos individuales (1 campo lleno)
    {"first_name": True,  "last_name": False, "email": False, "phone": False, "address": False, "city": False, "zip_code": False, "country": False, "success": False},
    {"first_name": False, "last_name": True,  "email": False, "phone": False, "address": False, "city": False, "zip_code": False, "country": False, "success": False},
    {"first_name": False, "last_name": False, "email": True,  "phone": False, "address": False, "city": False, "zip_code": False, "country": False, "success": False},
    {"first_name": False, "last_name": False, "email": False, "phone": True,  "address": False, "city": False, "zip_code": False, "country": False, "success": False},
    {"first_name": False, "last_name": False, "email": False, "phone": False, "address": True,  "city": False, "zip_code": False, "country": False, "success": False},
    {"first_name": False, "last_name": False, "email": False, "phone": False, "address": False, "city": True,  "zip_code": False, "country": False, "success": False},
    {"first_name": False, "last_name": False, "email": False, "phone": False, "address": False, "city": False, "zip_code": True,  "country": False, "success": False},
    {"first_name": False, "last_name": False, "email": False, "phone": False, "address": False, "city": False, "zip_code": False, "country": True,  "success": False},

    # Happy path (todos llenos)
    {"first_name": True, "last_name": True, "email": True, "phone": True, "address": True, "city": True, "zip_code": True, "country": True, "success": True},
]

@pytest.mark.parametrize("case", checkout_cases)
def test_checkout_fields(driver, case):
    home_page = HomePage(driver)
    category_page = CategoryPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    # Flujo rápido hasta Checkout
    home_page.load()
    home_page.go_to_women_clothes()
    category_page.wait_for_women_clothes_page()
    category_page.wait_for_products_loaded()

    product_id = category_page.get_product_ids_in_page()[0]
    product_name = category_page.get_product_name(product_id)
    category_page.add_product_and_validate_badge(product_id)

    home_page.go_to_cart()
    cart_page.wait_for_cart_loaded(with_products=True)
    cart_page.proceed_to_checkout_and_validate()
    assert checkout_page.is_loaded()
    assert checkout_page.is_customer_info_loaded()

    # Validar que labels estén correctos
    assert checkout_page.validate_field_labels(), "❌ Los labels no coinciden con lo esperado"

    # Llenar formulario dependiendo del caso
    checkout_page.fill_checkout_form(
        first_name=random_first_name() if case["first_name"] else "",
        last_name=random_last_name() if case["last_name"] else "",
        email=random_email() if case["email"] else "",
        phone=random_phone() if case["phone"] else "",
        address=random_address() if case["address"] else "",
        city=random_city() if case["city"] else "",
        zip_code=random_zip_code() if case["zip_code"] else "",
        country=random_country() if case["country"] else "",
    )

    checkout_page.place_order()
    alert_text = checkout_page.handle_alert_and_get_text()

    if case["success"]:
        expected_url = os.getenv("UI_CHECKOUT_COMPLETE_URL")
        assert driver.current_url == expected_url, (
            f"❌ No se redirigió a la URL esperada. "
            f"Esperado: {expected_url}, encontrado: {driver.current_url}"
        )

    else:
        assert alert_text == "Please fill in all required fields", f"❌ Alerta incorrecta: {alert_text}"

        # Luego validar que la URL NO cambió
        expected_url = os.getenv("UI_CHECKOUT_COMPLETE_URL")
        assert driver.current_url != expected_url, (
            f"❌ Checkout avanzó aunque faltaban campos obligatorios. "
            f"URL actual: {driver.current_url}"
        )


# -----------------------------------
# Caso especial: email inválido
# -----------------------------------
def test_checkout_invalid_email_format(driver):
    home_page = HomePage(driver)
    category_page = CategoryPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    # Flujo rápido hasta Checkout
    home_page.load()
    home_page.go_to_women_clothes()
    category_page.wait_for_women_clothes_page()
    category_page.wait_for_products_loaded()

    product_id = category_page.get_product_ids_in_page()[0]
    product_name = category_page.get_product_name(product_id)
    category_page.add_product_and_validate_badge(product_id)

    home_page.go_to_cart()
    cart_page.wait_for_cart_loaded(with_products=True)
    cart_page.proceed_to_checkout_and_validate()
    assert checkout_page.is_loaded()
    assert checkout_page.is_customer_info_loaded()

    # Generamos un email inválido
    invalid_email = random_first_name()

    checkout_page.fill_checkout_form(
        first_name=random_first_name(),
        last_name=random_last_name(),
        email=invalid_email,  # inválido
        phone=random_phone(),
        address=random_address(),
        city=random_city(),
        zip_code=random_zip_code(),
        country=random_country(),
    )

    checkout_page.place_order()

    expected_url = os.getenv("UI_CHECKOUT_COMPLETE_URL")
    assert driver.current_url != expected_url, (
        f"❌ Checkout permitió avanzar con email inválido: {invalid_email}"
    )
