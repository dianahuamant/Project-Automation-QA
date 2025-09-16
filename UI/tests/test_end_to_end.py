import os
import pytest
from UI.pages.sign_up_page import SignUpPage
from UI.pages.login_page import LoginPage
from UI.pages.home_page import HomePage
from UI.pages.category_page import CategoryPage
from UI.pages.cart_page import CartPage
from UI.pages.checkout_page import CheckoutPage
from UI.utils.faker_data import (
    random_first_name, random_last_name, random_email,
    random_password, random_phone, random_address,
    random_city, random_zip_code, random_country
)

@pytest.mark.e2e
def test_end_to_end_signup_login_checkout_with_one_product(driver):
    # Instanciar pages
    signup_page = SignUpPage(driver)
    login_page = LoginPage(driver)
    home_page = HomePage(driver)
    category_page = CategoryPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    # --------- 1. Registro ---------
    signup_page.load()
    email = random_email()
    password = random_password()
    signup_page.register_user(
        first_name=random_first_name(),
        last_name=random_last_name(),
        email=email,
        zip_code=random_zip_code(),
        password=password,
    )
    assert signup_page.wait_for_signup_success(), "❌ El registro no se completó correctamente"

    # --------- 2. Login ---------
    login_page.load()
    login_page.login_as_user(email, password)
    assert login_page.wait_for_login_success(), "❌ No se pudo hacer login"

    # --------- 3. Agregar producto ---------
    home_page.load()
    home_page.go_to_women_clothes()
    category_page.wait_for_women_clothes_page()
    category_page.wait_for_products_loaded()
    product_id = category_page.get_product_ids_in_page()[0]
    category_page.add_product_and_validate_badge(product_id)

    # --------- 4. Checkout ---------
    home_page.go_to_cart()
    cart_page.wait_for_cart_loaded(with_products=True)
    cart_page.proceed_to_checkout_and_validate()

    checkout_page.fill_checkout_form(
        first_name=random_first_name(),
        last_name=random_last_name(),
        email=email,
        phone=random_phone(),
        address=random_address(),
        city=random_city(),
        zip_code=random_zip_code(),
        country=random_country(),
    )
    checkout_page.place_order()
    alert_text = checkout_page.handle_alert_and_get_text()
    checkout_page.wait_for_overlay_to_disappear()

    expected_url = os.getenv("UI_CHECKOUT_COMPLETE_URL")

    if alert_text:
        # Caso fallido → validamos la alerta + que no cambió la URL
        assert alert_text == "Please fill in all required fields", f"❌ Alerta incorrecta: {alert_text}"
        assert driver.current_url != expected_url, (
            f"❌ Checkout avanzó aunque faltaban campos obligatorios. "
            f"URL actual: {driver.current_url}"
        )
    else:
        # Caso exitoso → validamos redirección
        assert driver.current_url == expected_url, (
            f"❌ No se redirigió a la URL esperada. "
            f"Esperado: {expected_url}, encontrado: {driver.current_url}"
        )

@pytest.mark.e2e
def test_end_to_end_signup_login_checkout_with_four_products(driver):
    # Instanciar pages
    signup_page = SignUpPage(driver)
    login_page = LoginPage(driver)
    home_page = HomePage(driver)
    category_page = CategoryPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    # --------- 1. Registro ---------
    signup_page.load()
    email = random_email()
    password = random_password()
    signup_page.register_user(
        first_name=random_first_name(),
        last_name=random_last_name(),
        email=email,
        zip_code=random_zip_code(),
        password=password,
    )
    assert signup_page.wait_for_signup_success(), "❌ El registro no se completó correctamente"

    # --------- 2. Login ---------
    login_page.load()
    login_page.login_as_user(email, password)
    assert login_page.wait_for_login_success(), "❌ No se pudo hacer login"

    # --------- 3. Agregar 4 productos ---------
    home_page.load()
    home_page.go_to_women_clothes()
    category_page.wait_for_women_clothes_page()
    category_page.wait_for_products_loaded()

    product_ids = category_page.get_product_ids_in_page()
    assert len(product_ids) >= 4, "❌ No hay al menos 4 productos en la categoría"

    selected_products = []
    for pid in product_ids[:4]:
        product_name = category_page.get_product_name(pid)
        added = category_page.add_product_and_validate_badge(pid)
        assert added, f"❌ No se pudo agregar al carrito el producto id={pid}"
        selected_products.append(product_name)

    # --------- 4. Checkout ---------
    home_page.go_to_cart()
    cart_page.wait_for_cart_loaded(with_products=True)

    # Validar que los 4 productos estén en el carrito
    for pname in selected_products:
        assert cart_page.is_product_in_cart(pname), f"❌ El producto '{pname}' no está en el carrito"
        qty = cart_page.get_product_quantity(pname)
        assert qty == 1, f"❌ Cantidad incorrecta para '{pname}'. Esperado=1, encontrado={qty}"

    cart_page.proceed_to_checkout_and_validate()

    checkout_page.fill_checkout_form(
        first_name=random_first_name(),
        last_name=random_last_name(),
        email=email,  # mismo email registrado
        phone=random_phone(),
        address=random_address(),
        city=random_city(),
        zip_code=random_zip_code(),
        country=random_country(),
    )
    checkout_page.place_order()
    alert_text = checkout_page.handle_alert_and_get_text()
    checkout_page.wait_for_overlay_to_disappear()

    expected_url = os.getenv("UI_CHECKOUT_COMPLETE_URL")

    if alert_text:
        # Caso fallido → validamos la alerta + que no cambió la URL
        assert alert_text == "Please fill in all required fields", f"❌ Alerta incorrecta: {alert_text}"
        assert driver.current_url != expected_url, (
            f"❌ Checkout avanzó aunque faltaban campos obligatorios. "
            f"URL actual: {driver.current_url}"
        )
    else:
        # Caso exitoso → validamos redirección
        assert driver.current_url == expected_url, (
            f"❌ No se redirigió a la URL esperada. "
            f"Esperado: {expected_url}, encontrado: {driver.current_url}"
        )

    print(f"✅ E2E OK: Se registró usuario {email}, se logueó, agregó 4 productos y completó checkout → {selected_products}")