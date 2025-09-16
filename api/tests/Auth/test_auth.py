import pytest
import requests
from api.utils.api_client import APIClient
from faker import Faker

# ----------------- Pruebas para Signup' -----------------

def test_signup_successful(created_passenger_user_info):
    """
    Test que verifica el registro exitoso de un nuevo usuario 'passenger'
    validando principalmente el body response.
    """
    # Validamos directamente los datos retornados por el fixture
    assert "id" in created_passenger_user_info
    assert isinstance(created_passenger_user_info["id"], str)
    assert "email" in created_passenger_user_info
    assert "full_name" in created_passenger_user_info

    # Rol por defecto
    assert created_passenger_user_info.get("role", "passenger") == "passenger"

def test_signup_unsuccessful_missing_fields(api_client):
    """
    Test que verifica que el registro falla cuando faltan campos obligatorios.
    """

    payload_invalido = {}

    response = api_client.post("/auth/signup", data=payload_invalido)

    assert response.status_code == 422

    # Verifica que la respuesta JSON contenga el campo "detail".
    response_data = response.json()
    assert "detail" in response_data
    assert isinstance(response_data["detail"], list)
    assert len(response_data["detail"]) > 0


def test_signup_email_already_registered(api_client, created_passenger_user_info):
    """
    Verifica que la API devuelve un error 400 cuando se usa un email ya registrado.
    """
    signup_payload = {
        "email": created_passenger_user_info["email"],
        "password": created_passenger_user_info["password"],
        "full_name": created_passenger_user_info["full_name"],
    }
    second_response = api_client.post("/auth/signup", data=signup_payload)

    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Email already registered"

# ----------------- Pruebas para Login' -----------------

def test_login_successful(created_passenger_user_info, api_client):
    """
    Verifica que el login es exitoso usando un usuario recién registrado.
    """
    login_payload = {
        "username": created_passenger_user_info["email"],
        "password": created_passenger_user_info["password"],
    }
    login_response = api_client.post_form("/auth/login", data=login_payload)
    response_data = login_response.json()

    # Validar body directamente
    assert "access_token" in response_data
    assert "token_type" in response_data
    assert response_data["token_type"] == "bearer"


def test_login_unsuccessful_wrong_password(api_client, created_passenger_user_info):
    """
    Verifica que el login falle con una contraseña incorrecta.
    """
    login_payload = {
        "username": created_passenger_user_info["email"],
        "password": created_passenger_user_info["password"] + "incorrecto"
    }
    login_response = api_client.post_form(endpoint="/auth/login", data=login_payload)
    assert login_response.status_code == 401
    assert login_response.json()["detail"] == "Incorrect credentials"


def test_login_unsuccessful_wrong_username(api_client, created_passenger_user_info):
    """
    Verifica que el login falle con un nombre de usuario (email) incorrecto.
    """
    fake = Faker()
    login_payload = {
        "username": f"no-existe-{fake.uuid4()}@{fake.domain_name()}",
        "password": created_passenger_user_info["password"]
    }
    login_response = api_client.post_form(endpoint="/auth/login", data=login_payload)
    assert login_response.status_code == 401
    assert login_response.json()["detail"] == "Incorrect credentials"


def test_login_unsuccessful_both_incorrect(api_client):
    """
    Verifica que el login falle si el nombre de usuario y la contraseña son incorrectos.
    """
    fake = Faker()
    login_payload = {
        "username": f"no-existe-{fake.uuid4()}@{fake.domain_name()}",
        "password": "wrong-password",
    }
    login_response = api_client.post_form(endpoint="/auth/login", data=login_payload)
    assert login_response.status_code == 401
    assert login_response.json()["detail"] == "Incorrect credentials"

def test_login_with_json_payload(api_client, created_passenger_user_info):
    """
    Verifica que la API rechace el login si el payload se envía en formato JSON (422).
    """
    login_payload_json = {
        "username": created_passenger_user_info["email"],
        "password": created_passenger_user_info["password"],
    }
    login_url = f"{api_client.base_url}/auth/login"
    login_response = requests.post(login_url, json=login_payload_json)
    assert login_response.status_code == 422
    assert login_response.json()["detail"][0]["type"] == "missing"
    assert "Field required" in login_response.json()["detail"][0]["msg"]