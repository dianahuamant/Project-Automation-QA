import pytest
from faker import Faker
from api.utils.api_client import APIClient

## ----------------- Pruebas de Create Aircraft -----------------
# ----------------- Pruebas para el campo 'tail_number' (Valores Límite) -----------------

def test_aircraft_with_invalid_tail_number_length_4(auth_api_client, aircraft_payload):
    """
    Verifica que la API rechace un 'tail_number' con 4 caracteres.
    """
    fake = Faker()
    payload = aircraft_payload.copy()
    payload["tail_number"] = fake.password(length=4, special_chars=False).upper()
    response = auth_api_client.post(endpoint="/aircrafts", data=payload)
    assert response.status_code == 422
    assert "String should have at least 5 characters" in response.json()["detail"][0]["msg"]

def test_aircraft_with_valid_tail_number_length_5(auth_api_client, aircraft_payload):
    """
    Verifica que la API acepta un 'tail_number' con 5 caracteres.
    """
    fake = Faker()
    payload = aircraft_payload.copy()
    payload["tail_number"] = fake.password(length=5, special_chars=False).upper()
    response = auth_api_client.post(endpoint="/aircrafts", data=payload)
    assert response.status_code == 201

def test_aircraft_with_valid_tail_number_length_9(auth_api_client, aircraft_payload):
    """
    Verifica que la API acepta un 'tail_number' con 9 caracteres.
    """
    fake = Faker()
    payload = aircraft_payload.copy()
    payload["tail_number"] = fake.password(length=9, special_chars=False).upper()
    response = auth_api_client.post(endpoint="/aircrafts", data=payload)
    assert response.status_code == 201

def test_aircraft_with_valid_tail_number_length_10(auth_api_client, aircraft_payload):
    """
    Verifica que la API acepta un 'tail_number' con 10 caracteres.
    """
    fake = Faker()
    payload = aircraft_payload.copy()
    payload["tail_number"] = fake.password(length=10, special_chars=False).upper()
    response = auth_api_client.post(endpoint="/aircrafts", data=payload)
    assert response.status_code == 201

def test_aircraft_with_invalid_tail_number_length_11(auth_api_client, aircraft_payload):
    """
    Verifica que la API rechace un 'tail_number' con 11 caracteres.
    """
    fake = Faker()
    payload = aircraft_payload.copy()
    payload["tail_number"] = fake.password(length=11, special_chars=False).upper()
    response = auth_api_client.post(endpoint="/aircrafts", data=payload)
    assert response.status_code == 422
    assert "String should have at most 10 characters" in response.json()["detail"][0]["msg"]

# ----------------- Pruebas para el campo 'model' -----------------

def test_aircraft_with_valid_model_string(auth_api_client, aircraft_payload):
    """
    Verifica que la API acepta un 'model' que es un string.
    """
    response = auth_api_client.post(endpoint="/aircrafts", data=aircraft_payload)
    assert response.status_code == 201

def test_aircraft_with_non_string_model(auth_api_client, aircraft_payload):
    """
    Verifica que la API rechace un 'model' que no sea un string.
    """
    payload = aircraft_payload.copy()
    payload["model"] = 12345
    response = auth_api_client.post(endpoint="/aircrafts", data=payload)
    assert response.status_code == 422
    assert "Input should be a valid string" in response.json()["detail"][0]["msg"]

# ----------------- Pruebas para el campo 'capacity' -----------------

def test_aircraft_with_negative_capacity(auth_api_client, aircraft_payload):
    """
    Verifica que la API rechace una 'capacity' que sea negativa porque no puedes tener una aeronave con capacidad negativa de personas.
    """
    payload = aircraft_payload.copy()
    payload["capacity"] = -10
    response = auth_api_client.post(endpoint="/aircrafts", data=payload)
    assert response.status_code == 422

# ----------------- Pruebas de Get Aircraft -----------------

def test_get_aircrafts_with_non_integer_skip(api_client):
    """
    Verifica que la API rechace una petición con un 'skip' que no es un entero.
    """
    params = {"skip": "abc", "limit": 1}
    response = api_client.get(endpoint="/aircrafts", params=params)

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "int_parsing"


def test_get_aircrafts_with_non_integer_limit(api_client):
    """
    Verifica que la API rechace una petición con un 'limit' que no es un entero.
    """
    params = {"skip": 0, "limit": "abc"}
    response = api_client.get(endpoint="/aircrafts", params=params)

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "int_parsing"


def test_get_aircrafts_with_negative_skip(api_client):
    """
    Verifica que la API rechace una petición con un 'skip' negativo.
    """
    params = {"skip": -1, "limit": 10}
    response = api_client.get(endpoint="/aircrafts", params=params)

    assert response.status_code == 422


def test_get_aircrafts_with_negative_limit(api_client):
    """
    Verifica que la API rechace una petición con un 'limit' negativo.
    """
    params = {"skip": 0, "limit": -1}
    response = api_client.get(endpoint="/aircrafts", params=params)

    assert response.status_code == 422

def test_get_aircrafts_with_limit_equal_to_zero(api_client):
    """
    Verifica que la API devuelva una lista vacía con 'limit=0'.
    """
    params = {"skip": 0, "limit": 0}
    response = api_client.get(endpoint="/aircrafts", params=params)

    assert response.status_code == 200
    assert response.json() == []

def test_get_aircrafts_with_skip_equal_to_zero(api_client):
    """
    Verifica que la API acepte 'skip=0' y devuelva resultados.
    """
    params = {"skip": 0, "limit": 2}
    response = api_client.get(endpoint="/aircrafts", params=params)

    assert response.status_code == 200
    assert len(response.json()) == 2

# ----------------- Pruebas de Get Aircraft por ID-----------------

def test_get_aircraft_with_invalid_id_format_returns_404(api_client):
    """
    Verifica que la API devuelva 404 Not Found si el ID del avión tiene formato incorrecto.
    """
    invalid_id = "12345"
    response = api_client.get(endpoint=f"/aircrafts/{invalid_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"


def test_get_aircraft_with_non_existent_id_returns_404(api_client):
    """
    Verifica que la API devuelva 404 Not Found si el ID del avión no existe.
    """
    non_existent_id = "acf-xxxxxxxxxxxx"  # Un ID con formato válido, pero que no está en la base de datos
    response = api_client.get(endpoint=f"/aircrafts/{non_existent_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"

# ----------------- Pruebas para Actualizar Aircraft-----------------

def test_update_aircraft_with_invalid_tail_number_length_4(api_client, admin_token, aircraft_payload):
    """
    Verifica que la API rechace una actualización con un 'tail_number' de 4 caracteres.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    creation_response = admin_api_client.post(endpoint="/aircrafts", data=aircraft_payload)
    assert creation_response.status_code == 201
    aircraft_id_to_update = creation_response.json()["id"]

    fake = Faker()
    update_payload = {
        "tail_number": fake.password(length=4, special_chars=False).upper(),
        "model": aircraft_payload["model"],
        "capacity": aircraft_payload["capacity"]
    }
    response = admin_api_client.put(endpoint=f"/aircrafts/{aircraft_id_to_update}", json_data=update_payload)

    assert response.status_code == 422
    assert "String should have at least 5 characters" in response.json()["detail"][0]["msg"]


def test_update_aircraft_with_valid_tail_number_length_5(api_client, admin_token, aircraft_payload):
    """
    Verifica que la API acepte una actualización con un 'tail_number' de 5 caracteres.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    creation_response = admin_api_client.post(endpoint="/aircrafts", data=aircraft_payload)
    assert creation_response.status_code == 201
    aircraft_id_to_update = creation_response.json()["id"]

    fake = Faker()
    update_payload = {
        "tail_number": fake.password(length=5, special_chars=False).upper(),
        "model": aircraft_payload["model"],
        "capacity": aircraft_payload["capacity"]
    }
    response = admin_api_client.put(endpoint=f"/aircrafts/{aircraft_id_to_update}", json_data=update_payload)

    assert response.status_code == 200


def test_update_aircraft_with_valid_tail_number_length_9(api_client, admin_token, aircraft_payload):
    """
    Verifica que la API acepte una actualización con un 'tail_number' de 9 caracteres.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    creation_response = admin_api_client.post(endpoint="/aircrafts", data=aircraft_payload)
    assert creation_response.status_code == 201
    aircraft_id_to_update = creation_response.json()["id"]

    fake = Faker()
    update_payload = {
        "tail_number": fake.password(length=9, special_chars=False).upper(),
        "model": aircraft_payload["model"],
        "capacity": aircraft_payload["capacity"]
    }
    response = admin_api_client.put(endpoint=f"/aircrafts/{aircraft_id_to_update}", json_data=update_payload)

    assert response.status_code == 200


def test_update_aircraft_with_valid_tail_number_length_10(api_client, admin_token, aircraft_payload):
    """
    Verifica que la API acepte una actualización con un 'tail_number' de 10 caracteres.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    creation_response = admin_api_client.post(endpoint="/aircrafts", data=aircraft_payload)
    assert creation_response.status_code == 201
    aircraft_id_to_update = creation_response.json()["id"]

    fake = Faker()
    update_payload = {
        "tail_number": fake.password(length=10, special_chars=False).upper(),
        "model": aircraft_payload["model"],
        "capacity": aircraft_payload["capacity"]
    }
    response = admin_api_client.put(endpoint=f"/aircrafts/{aircraft_id_to_update}", json_data=update_payload)

    assert response.status_code == 200


def test_update_aircraft_with_invalid_tail_number_length_11(api_client, admin_token, aircraft_payload):
    """
    Verifica que la API rechace una actualización con un 'tail_number' de 11 caracteres.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    creation_response = admin_api_client.post(endpoint="/aircrafts", data=aircraft_payload)
    assert creation_response.status_code == 201
    aircraft_id_to_update = creation_response.json()["id"]

    fake = Faker()
    update_payload = {
        "tail_number": fake.password(length=11, special_chars=False).upper(),
        "model": aircraft_payload["model"],
        "capacity": aircraft_payload["capacity"]
    }
    response = admin_api_client.put(endpoint=f"/aircrafts/{aircraft_id_to_update}", json_data=update_payload)

    assert response.status_code == 422
    assert "String should have at most 10 characters" in response.json()["detail"][0]["msg"]


def test_update_aircraft_with_non_string_model(api_client, admin_token, aircraft_payload):
    """
    Verifica que la API rechace una actualización con un 'model' que no sea un string.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    creation_response = admin_api_client.post(endpoint="/aircrafts", data=aircraft_payload)
    assert creation_response.status_code == 201
    aircraft_id_to_update = creation_response.json()["id"]

    update_payload = {
        "tail_number": aircraft_payload["tail_number"],
        "model": 12345,
        "capacity": aircraft_payload["capacity"]
    }
    response = admin_api_client.put(endpoint=f"/aircrafts/{aircraft_id_to_update}", json_data=update_payload)

    assert response.status_code == 422
    assert "Input should be a valid string" in response.json()["detail"][0]["msg"]


def test_update_aircraft_with_non_integer_capacity(api_client, admin_token, aircraft_payload):
    """
    Verifica que la API rechace una actualización con una 'capacity' que no es un entero.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    creation_response = admin_api_client.post(endpoint="/aircrafts", data=aircraft_payload)
    assert creation_response.status_code == 201
    aircraft_id_to_update = creation_response.json()["id"]

    update_payload = {
        "tail_number": aircraft_payload["tail_number"],
        "model": aircraft_payload["model"],
        "capacity": "abc"
    }
    response = admin_api_client.put(endpoint=f"/aircrafts/{aircraft_id_to_update}", json_data=update_payload)

    assert response.status_code == 422
    assert "Input should be a valid integer" in response.json()["detail"][0]["msg"]


def test_update_aircraft_with_negative_capacity(api_client, admin_token, aircraft_payload):
    """
    Verifica que la API rechace una actualización con una 'capacity' negativa.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    creation_response = admin_api_client.post(endpoint="/aircrafts", data=aircraft_payload)
    assert creation_response.status_code == 201
    aircraft_id_to_update = creation_response.json()["id"]

    update_payload = {
        "tail_number": aircraft_payload["tail_number"],
        "model": aircraft_payload["model"],
        "capacity": -10
    }
    response = admin_api_client.put(endpoint=f"/aircrafts/{aircraft_id_to_update}", json_data=update_payload)

    assert response.status_code == 422