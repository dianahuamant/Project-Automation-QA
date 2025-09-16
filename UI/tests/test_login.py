import pytest
import os
from dotenv import load_dotenv
from UI.pages.login_page import LoginPage
from UI.utils.faker_data import random_email, random_password, random_first_name

load_dotenv()

LOGIN_SUCCESS_URL = os.getenv("UI_LOGIN_SUCCESS_URL")


@pytest.mark.parametrize("case", [
    {"email": True, "password": True, "success": True},   # Caso válido (Happy Path)
    {"email": False, "password": True, "success": False}, # Falta email
    {"email": True, "password": False, "success": False}, # Falta password
    {"email": False, "password": False, "success": False} # Falta todo
])
def test_login_obligatoriedad(driver, case):
    login = LoginPage(driver)
    login.load()

    email = random_email() if case["email"] else ""
    password = random_password() if case["password"] else ""

    login.login_as_user(email, password)

    if case["success"]:
        assert login.wait_for_login_success(), "El login debería ser exitoso"
    else:
        assert driver.current_url != LOGIN_SUCCESS_URL, "Se permitió login sin todos los campos obligatorios"


def test_login_invalid_email_format(driver):
    """Validar que email con formato incorrecto no permite login"""
    login = LoginPage(driver)
    login.load()

    invalid_email = random_first_name()
    password = random_password()

    login.login_as_user(invalid_email, password)

    assert driver.current_url != LOGIN_SUCCESS_URL, "Se permitió login con un email inválido"
