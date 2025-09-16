import pytest
import requests
from faker import Faker
# ----------------- Pruebas para los campos en Signup -----------------

# ----------------- Pruebas para el campo 'email' -----------------

def test_signup_with_valid_email(api_client, signup_payload):
    """
    Verifica que el registro es exitoso con un email de formato correcto.
    """
    response = api_client.post("/auth/signup", data=signup_payload)
    assert response.status_code == 201


def test_signup_invalid_email_format(api_client, signup_payload):
    """
    Verifica que la API rechace una petición con un email de formato inválido.
    """
    signup_payload["email"] = "not-an-email"
    response = api_client.post("/auth/signup", data=signup_payload)

    assert response.status_code == 422
    error_detail = response.json()["detail"][0]
    assert error_detail["type"] == "value_error"
    assert error_detail["loc"][1] == "email"
    assert "An email address must have an @-sign." in error_detail["msg"]

# ----------------- Pruebas para el campo 'password' (Valores Límite) -----------------

def test_signup_password_exactly_6_characters(api_client, signup_payload):
    """
    Verifica que el registro es exitoso con una contraseña de 6 caracteres.
    """
    fake = Faker()
    signup_payload["password"] = fake.password(length=6)
    response = api_client.post("/auth/signup", data=signup_payload)
    assert response.status_code == 201


def test_signup_password_too_short(api_client, signup_payload):
    """
    Verifica que la API rechace una contraseña con menos de 6 caracteres.
    """
    fake = Faker()
    signup_payload["password"] = fake.password(length=5)
    response = api_client.post("/auth/signup", data=signup_payload)

    assert response.status_code == 422
    error_detail = response.json()["detail"][0]
    assert error_detail["type"] == "string_too_short"
    assert error_detail["loc"][1] == "password"
    assert "String should have at least 6 characters" in error_detail["msg"]
    assert error_detail["ctx"]["min_length"] == 6


def test_signup_password_more_than_6_characters(api_client, signup_payload):
    """
    Verifica que el registro funciona con una contraseña de más de 6 caracteres.
    """
    fake = Faker()
    signup_payload["password"] = fake.password(length=7)
    response = api_client.post("/auth/signup", data=signup_payload)
    assert response.status_code == 201

# ----------------- Pruebas para el campo 'full_name' -----------------

def test_signup_with_valid_full_name(api_client, signup_payload):
    """
    Verifica que el registro es exitoso cuando se envía un full_name válido (string).
    """
    response = api_client.post("/auth/signup", data=signup_payload)
    assert response.status_code == 201


def test_signup_with_non_string_full_name(api_client, signup_payload):
    """
    Verifica que la API rechace el registro si 'full_name' no es un string.
    """
    signup_payload["full_name"] = 12345
    response = api_client.post("/auth/signup", data=signup_payload)

    assert response.status_code == 422
    error_detail = response.json()["detail"][0]
    assert error_detail["type"] == "string_type"
    assert error_detail["loc"][1] == "full_name"
    assert error_detail["msg"] == "Input should be a valid string"

# ----------------- Pruebas para los campos en Login -----------------

# ----------------- Pruebas para el campo 'username' -----------------

def test_login_successful_with_valid_string_username(api_client, created_passenger_user_info):
    """
    Verifica que el login es exitoso con un username que es un string.
    """
    login_payload = {
        "username": created_passenger_user_info["email"],
        "password": created_passenger_user_info["password"],
    }
    login_response = api_client.post_form(endpoint="/auth/login", data=login_payload)

    assert login_response.status_code == 200

    response_data = login_response.json()
    assert "access_token" in response_data
    assert "token_type" in response_data
    assert response_data["token_type"] == "bearer"

def test_login_unsuccessful_non_string_username(api_client, created_passenger_user_info):
    """
    Verifica que el login falle cuando el username es un tipo de dato incorrecto (ej. un número).
    """
    login_payload = {
        "username": 12345678,
        "password": created_passenger_user_info["password"],
    }

    login_response = api_client.post_form(endpoint="/auth/login", data=login_payload)

    assert login_response.status_code == 401
    assert login_response.json()["detail"] == "Incorrect credentials"

# ----------------- Pruebas para el campo 'password' -----------------

def test_login_successful_with_valid_string_password(api_client, created_passenger_user_info):
    """
    Verifica que el login es exitoso cuando el password es un string válido.
    """
    login_payload = {
        "username": created_passenger_user_info["email"],
        "password": created_passenger_user_info["password"],
    }

    login_response = api_client.post_form(endpoint="/auth/login", data=login_payload)

    assert login_response.status_code == 200

    response_data = login_response.json()
    assert "access_token" in response_data
    assert "token_type" in response_data
    assert response_data["token_type"] == "bearer"

def test_login_unsuccessful_non_string_password(api_client, created_passenger_user_info):
    """
    Verifica que el login falle cuando el password es un tipo de dato incorrecto (ej. un número).
    """
    login_payload = {
        "username": created_passenger_user_info["email"],
        "password": 12345678,
    }
    login_response = api_client.post_form(endpoint="/auth/login", data=login_payload)
    assert login_response.status_code == 401
    assert login_response.json()["detail"] == "Incorrect credentials"