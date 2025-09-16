import pytest
from UI.pages.sign_up_page import SignUpPage
from UI.utils.faker_data import random_first_name, random_last_name, random_email, random_zip_code, random_password
import os
from dotenv import load_dotenv

load_dotenv()
SIGNUP_SUCCESS_URL = os.getenv("UI_SIGNUP_SUCCESS_URL")

# -----------------------------------
# Lista de casos de prueba para validar obligatoriedad de campos (26 escenarios)
# -----------------------------------
signup_cases = [
    # Casos individuales
    {"first_name": True,  "last_name": False, "email": False, "zip_code": False, "password": False, "success": False},
    {"first_name": False, "last_name": True,  "email": False, "zip_code": False, "password": False, "success": False},
    {"first_name": False, "last_name": False, "email": True,  "zip_code": False, "password": False, "success": False},
    {"first_name": False, "last_name": False, "email": False, "zip_code": True,  "password": False, "success": False},
    {"first_name": False, "last_name": False, "email": False, "zip_code": False, "password": True,  "success": False},

    # Combinaciones de dos campos
    {"first_name": True,  "last_name": True,  "email": False, "zip_code": False, "password": False, "success": False},
    {"first_name": True,  "last_name": False, "email": True,  "zip_code": False, "password": False, "success": False},
    {"first_name": True,  "last_name": False, "email": False, "zip_code": True,  "password": False, "success": False},
    {"first_name": True,  "last_name": False, "email": False, "zip_code": False, "password": True,  "success": False},
    {"first_name": False, "last_name": True,  "email": True,  "zip_code": False, "password": False, "success": False},
    {"first_name": False, "last_name": True,  "email": False, "zip_code": True,  "password": False, "success": False},
    {"first_name": False, "last_name": True,  "email": False, "zip_code": False, "password": True,  "success": False},
    {"first_name": False, "last_name": False, "email": True,  "zip_code": True,  "password": False, "success": False},
    {"first_name": False, "last_name": False, "email": True,  "zip_code": False, "password": True,  "success": False},
    {"first_name": False, "last_name": False, "email": False, "zip_code": True,  "password": True,  "success": False},

    # Combinaciones de tres campos
    {"first_name": True,  "last_name": True,  "email": True,  "zip_code": False, "password": False, "success": False},
    {"first_name": True,  "last_name": True,  "email": False, "zip_code": True,  "password": False, "success": False},
    {"first_name": True,  "last_name": True,  "email": False, "zip_code": False, "password": True,  "success": False},
    {"first_name": True,  "last_name": False, "email": True,  "zip_code": True,  "password": False, "success": False},
    {"first_name": True,  "last_name": False, "email": True,  "zip_code": False, "password": True,  "success": False},
    {"first_name": True,  "last_name": False, "email": False, "zip_code": True,  "password": True,  "success": False},
    {"first_name": False, "last_name": True,  "email": True,  "zip_code": True,  "password": False, "success": False},
    {"first_name": False, "last_name": True,  "email": True,  "zip_code": False, "password": True,  "success": False},
    {"first_name": False, "last_name": True,  "email": False, "zip_code": True,  "password": True,  "success": False},
    {"first_name": False, "last_name": False, "email": True,  "zip_code": True,  "password": True,  "success": False},

    # Happy Path positivo (todos los campos)
    {"first_name": True,  "last_name": True,  "email": True,  "zip_code": True,  "password": True,  "success": True},
]

# -----------------------------------
# Test parametrizado para casos de obligatoriedad
# -----------------------------------
@pytest.mark.parametrize("case", signup_cases)
def test_signup_fields(driver, case):
    signup = SignUpPage(driver)
    signup.load()

    signup.register_user(
        first_name=random_first_name() if case["first_name"] else "",
        last_name=random_last_name() if case["last_name"] else "",
        email=random_email() if case["email"] else "",
        zip_code=random_zip_code() if case["zip_code"] else "",
        password=random_password() if case["password"] else ""
    )

    if case["success"]:
        assert signup.wait_for_signup_success(), "No se mostró mensaje de registro exitoso"
    else:
        assert not signup.wait_for_signup_success(), "Se permitió registro aunque faltaban campos obligatorios"

def test_signup_invalid_email_format(driver):
    signup = SignUpPage(driver)
    signup.load()

    # Generamos un "email" inválido usando solo un nombre aleatorio
    invalid_email = random_first_name()

    signup.register_user(
        first_name=random_first_name(),
        last_name=random_last_name(),
        email=invalid_email,
        zip_code=random_zip_code(),
        password=random_password()
    )
    assert not signup.wait_for_signup_success(), f"Se permitió registro con email inválido: {invalid_email}"
