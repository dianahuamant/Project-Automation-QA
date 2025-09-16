import pytest
from faker import Faker
from api.utils.api_client import APIClient

# ----------------- Pruebas para Create User as Admin -----------------

# ----------------- Pruebas para el campo 'email' -----------------

def test_create_admin_user_with_valid_email(created_admin_user_info):
    """
    Verifica que la creación de usuario admin con un email válido es exitosa.
    """
    assert created_admin_user_info["role"] == "admin"
    assert "@" in created_admin_user_info["email"]
    assert created_admin_user_info["full_name"] != ""

def test_create_admin_user_with_invalid_email_format(auth_api_client, admin_signup_payload):
    """
    Verifica que la API rechace una petición con un email de formato inválido.
    """
    admin_signup_payload["email"] = "not-an-email"
    response = auth_api_client.post(endpoint="/users", data=admin_signup_payload)

    assert response.status_code == 422
    error_detail = response.json()["detail"][0]
    assert error_detail["type"] == "value_error"
    assert error_detail["loc"][1] == "email"
    assert "An email address must have an @-sign." in error_detail["msg"]

# ----------------- Pruebas para el campo 'password' (Valores Límite) -----------------

def test_create_admin_user_password_exactly_6_characters(auth_api_client, admin_signup_payload):
    """
    Verifica que la creación es exitosa con una contraseña de 6 caracteres.
    """
    fake = Faker()
    admin_signup_payload["password"] = fake.password(length=6)
    response = auth_api_client.post(endpoint="/users", data=admin_signup_payload)
    assert response.status_code == 201


def test_create_admin_user_password_too_short(auth_api_client, admin_signup_payload):
    """
    Verifica que la API rechace una contraseña con menos de 6 caracteres.
    """
    fake = Faker()
    admin_signup_payload["password"] = fake.password(length=5)
    response = auth_api_client.post(endpoint="/users", data=admin_signup_payload)

    assert response.status_code == 422
    error_detail = response.json()["detail"][0]
    assert error_detail["type"] == "string_too_short"
    assert error_detail["loc"][1] == "password"
    assert "String should have at least 6 characters" in error_detail["msg"]
    assert error_detail["ctx"]["min_length"] == 6


def test_create_admin_user_password_more_than_6_characters(auth_api_client, admin_signup_payload):
    """
    Verifica que la creación funciona con una contraseña de más de 6 caracteres.
    """
    fake = Faker()
    admin_signup_payload["password"] = fake.password(length=7)
    response = auth_api_client.post(endpoint="/users", data=admin_signup_payload)
    assert response.status_code == 201


# ----------------- Pruebas para el campo 'full_name' -----------------

def test_create_admin_user_with_valid_full_name(created_admin_user_info):
    """
    Verifica que la creación es exitosa cuando se envía un full_name válido (string).
    """
    assert created_admin_user_info["role"] == "admin"
    assert "@" in created_admin_user_info["email"]
    assert created_admin_user_info["full_name"] != ""


def test_create_admin_user_with_non_string_full_name(auth_api_client, admin_signup_payload):
    """
    Verifica que la API rechace la creación si 'full_name' no es un string.
    """
    admin_signup_payload["full_name"] = 12345
    response = auth_api_client.post(endpoint="/users", data=admin_signup_payload)

    assert response.status_code == 422
    error_detail = response.json()["detail"][0]
    assert error_detail["type"] == "string_type"
    assert error_detail["loc"][1] == "full_name"
    assert error_detail["msg"] == "Input should be a valid string"

# ----------------- Pruebas para el campo 'role' -----------------

def test_create_admin_user_with_valid_role(created_admin_user_info):
    """
    Verifica que la creación es exitosa cuando se envía un rol válido (admin).
    """
    assert created_admin_user_info["role"] == "admin"
    assert "@" in created_admin_user_info["email"]
    assert created_admin_user_info["full_name"] != ""


def test_create_admin_user_with_non_string_role(auth_api_client, admin_signup_payload):
    """
    Verifica que la API rechace la creación si 'role' no es un string
    y el mensaje de error sea el esperado.
    """
    # Usamos un valor inválido (un número) para el rol
    admin_signup_payload["role"] = 12345
    response = auth_api_client.post(endpoint="/users", data=admin_signup_payload)

    # Validamos que la API devuelve un error de tipo 'enum'
    assert response.status_code == 422
    error_detail = response.json()["detail"][0]
    assert error_detail["type"] == "enum"
    assert error_detail["loc"][1] == "role"
    assert error_detail["msg"] == "Input should be 'passenger' or 'admin'"

# ----------------- Pruebas para List Users -----------------

def test_get_users_with_valid_skip_and_limit(api_client, admin_token):
    """
    Verifica que si se envía 'skip' y 'limit' integer funciona correctamente.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)

    params = {"skip": 1, "limit": 2}
    response = admin_api_client.get(endpoint="/users", params=params)

    assert response.status_code == 200

    response_data = response.json()
    assert len(response_data) == 2
    assert isinstance(response_data, list)

def test_get_users_with_non_integer_skip(api_client, admin_token):
    """
    Verifica que la API rechace una petición con un 'skip' que no es un entero.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)

    params = {"skip": "abc", "limit": 1}
    response = admin_api_client.get(endpoint="/users", params=params)

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "int_parsing"


def test_get_users_with_non_integer_limit(api_client, admin_token):
    """
    Verifica que la API rechace una petición con un 'limit' que no es un entero.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)

    params = {"skip": 0, "limit": "abc"}
    response = admin_api_client.get(endpoint="/users", params=params)

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "int_parsing"


def test_get_users_with_negative_skip(api_client, admin_token):
    """
    Verifica que la API rechace una petición con un 'skip' negativo debido a que un skip no debe ser negativo.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)

    params = {"skip": -1, "limit": 10}
    response = admin_api_client.get(endpoint="/users", params=params)

    assert response.status_code == 422


def test_get_users_with_negative_limit(api_client, admin_token):
    """
    Verifica que la API rechace una petición con un 'limit' negativo debido a que un limit no debe ser negativo..
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)

    params = {"skip": 0, "limit": -1}
    response = admin_api_client.get(endpoint="/users", params=params)

    assert response.status_code == 422


def test_get_users_with_skip_equal_to_zero(api_client, admin_token):
    """
    Verifica que la API acepte 'skip=0' y devuelva resultados.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)

    params = {"skip": 0, "limit": 2}
    response = admin_api_client.get(endpoint="/users", params=params)

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_users_with_limit_equal_to_zero(api_client, admin_token):
    """
    Verifica que la API devuelva una lista vacía con 'limit=0'.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)

    params = {"skip": 0, "limit": 0}
    response = admin_api_client.get(endpoint="/users", params=params)

    assert response.status_code == 200
    assert response.json() == []

# ----------------- Pruebas para Update Users -----------------

def test_update_user_with_invalid_email_format(created_passenger_user_info, api_client):
    """
    Verifica que la API rechace la actualización si el email es inválido.
    """
    user_id = created_passenger_user_info["id"]
    user_api_client = APIClient(base_url=api_client.base_url, token=created_passenger_user_info["token"])

    update_payload = {
        "email": "not-an-email",
        "password": created_passenger_user_info["password"],
        "full_name": created_passenger_user_info["full_name"]
    }

    update_response = user_api_client.put(endpoint=f"/users/{user_id}", json_data=update_payload)

    assert update_response.status_code == 422
    assert "An email address must have an @-sign." in update_response.json()["detail"][0]["msg"]

def test_update_user_password_too_short(created_passenger_user_info, api_client):
    """
    Verifica que la API rechace la actualización si el password tiene menos de 6 caracteres.
    """
    user_id = created_passenger_user_info["id"]
    user_api_client = APIClient(base_url=api_client.base_url, token=created_passenger_user_info["token"])

    update_payload = {
        "email": created_passenger_user_info["email"],
        "password": "12345",  # Menos de 6 caracteres
        "full_name": created_passenger_user_info["full_name"]
    }

    update_response = user_api_client.put(endpoint=f"/users/{user_id}", json_data=update_payload)

    assert update_response.status_code == 422
    assert "String should have at least 6 characters" in update_response.json()["detail"][0]["msg"]


def test_update_user_with_non_string_full_name(created_passenger_user_info, api_client):
    """
    Verifica que la API rechace la actualización si 'full_name' no es un string.
    """
    user_id = created_passenger_user_info["id"]
    user_api_client = APIClient(base_url=api_client.base_url, token=created_passenger_user_info["token"])

    update_payload = {
        "email": created_passenger_user_info["email"],
        "password": created_passenger_user_info["password"],
        "full_name": 12345
    }

    update_response = user_api_client.put(endpoint=f"/users/{user_id}", json_data=update_payload)

    assert update_response.status_code == 422
    assert "Input should be a valid string" in update_response.json()["detail"][0]["msg"]