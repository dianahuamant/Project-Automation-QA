import pytest
from faker import Faker
from api.utils.api_client import APIClient

# ----------------- Pruebas para Create Airport -----------------
# ----------------- Pruebas para el campo 'iata_code' -----------------

def test_create_airport_with_valid_iata_code(created_airport_info):
    """
    Verifica que la API acepta un código IATA de 3 letras.
    """
    airport_data = created_airport_info

    assert "iata_code" in airport_data
    assert "city" in airport_data
    assert "country" in airport_data

    # Validar tipos
    assert isinstance(airport_data["iata_code"], str)
    assert isinstance(airport_data["city"], str)
    assert isinstance(airport_data["country"], str)

    # Validar patrón de iata_code
    assert len(airport_data["iata_code"]) == 3
    assert airport_data["iata_code"].isupper()

def test_create_airport_with_invalid_iata_code_length(auth_api_client, airport_payload):
    """
    Verifica que la API rechaza un código IATA que no tiene 3 letras.
    """
    airport_payload["iata_code"] = "ABCD"  # Longitud inválida
    response = auth_api_client.post(endpoint="/airports", data=airport_payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "String should match pattern '^[A-Z]{3}$'"

def test_create_airport_without_iata_code(auth_api_client, airport_payload):
    """
    Verifica que la API rechace la creación si no se envía el código IATA.
    """
    del airport_payload["iata_code"]
    response = auth_api_client.post(endpoint="/airports", data=airport_payload)
    assert response.status_code == 422
    assert "Field required" in response.json()["detail"][0]["msg"]

# ----------------- Pruebas para el campo 'city' -----------------

def test_create_airport_with_valid_city_string(created_airport_info):
    """
    Verifica que el city del aeropuerto creado sea un string.
    """
    airport_data = created_airport_info
    assert isinstance(airport_data["city"], str)
    assert len(airport_data["city"]) > 0

def test_create_airport_with_non_string_city(auth_api_client, airport_payload):
    """
    Verifica que la API rechace una ciudad que no sea un string.
    """
    fake = Faker()
    airport_payload["city"] = fake.random_int()  # Un número
    response = auth_api_client.post(endpoint="/airports", data=airport_payload)
    assert response.status_code == 422
    assert "Input should be a valid string" in response.json()["detail"][0]["msg"]

# ----------------- Pruebas para el campo 'country' -----------------

def test_create_airport_with_valid_country_string(created_airport_info):
    """
    Verifica que el country del aeropuerto creado sea un string.
    """
    airport_data = created_airport_info
    assert isinstance(airport_data["country"], str)
    assert len(airport_data["country"]) > 0

def test_create_airport_with_non_string_country(auth_api_client, airport_payload):
    """
    Verifica que la API rechace un país que no sea un string.
    """
    fake = Faker()
    airport_payload["country"] = fake.random_int()
    response = auth_api_client.post(endpoint="/airports", data=airport_payload)
    assert response.status_code == 422
    assert "Input should be a valid string" in response.json()["detail"][0]["msg"]

# ----------------- Pruebas para Get Airport -----------------

def test_get_airports_with_non_integer_skip(api_client):
    """
    Verifica que la API rechace una petición con un 'skip' que no es un entero.
    """
    params = {"skip": "abc", "limit": 1}
    response = api_client.get(endpoint="/airports", params=params)

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "int_parsing"


def test_get_airports_with_non_integer_limit(api_client):
    """
    Verifica que la API rechace una petición con un 'limit' que no es un entero.
    """
    params = {"skip": 0, "limit": "abc"}
    response = api_client.get(endpoint="/airports", params=params)

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "int_parsing"


def test_get_airports_with_negative_skip(api_client):
    """
    Verifica que la API rechace una petición con un 'skip' negativo.
    """
    params = {"skip": -1, "limit": 10}
    response = api_client.get(endpoint="/airports", params=params)

    assert response.status_code == 422


def test_get_airports_with_negative_limit(api_client):
    """
    Verifica que la API rechace una petición con un 'limit' negativo.
    """
    params = {"skip": 0, "limit": -1}
    response = api_client.get(endpoint="/airports", params=params)

    assert response.status_code == 422

def test_get_airports_with_limit_equal_to_zero(api_client):
    """
    Verifica que la API devuelva una lista vacía con 'limit=0'.
    """
    params = {"skip": 0, "limit": 0}
    response = api_client.get(endpoint="/airports", params=params)

    assert response.status_code == 200
    assert response.json() == []

def test_get_airports_with_skip_equal_to_zero(api_client):
    """
    Verifica que la API acepte 'skip=0' y devuelva resultados.
    """
    # skip=0 y limit=2, como en la segunda página
    params = {"skip": 0, "limit": 2}
    response = api_client.get(endpoint="/airports", params=params)

    assert response.status_code == 200
    assert len(response.json()) == 2

# ----------------- Pruebas para Listar aeropuertos según IATA CODE -----------------

def test_get_airport_with_invalid_iata_code_format_returns_404(api_client):
    """
    Verifica que la API devuelva 404 Not Found si el código IATA tiene formato incorrecto.
    """
    invalid_iata_code = "ABCD"
    response = api_client.get(endpoint=f"/airports/{invalid_iata_code}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"


def test_get_airport_with_numeric_iata_code_returns_404(api_client):
    """
    Verifica que la API devuelva 404 Not Found si se busca un IATA_CODE que es un número.
    """
    numeric_iata_code = "34"
    response = api_client.get(endpoint=f"/airports/{numeric_iata_code}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"

# ----------------- Pruebas para Update Airport -----------------

def test_update_airport_with_invalid_iata_code_length(api_client, admin_token, created_airport_info):
    """
    Verifica que la API rechaza una actualización si el código IATA no cumple el patrón.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    iata_code_to_update = created_airport_info["iata_code"]

    update_payload = {
        "iata_code": "ABCD",  # Longitud inválida que no cumple el patrón
        "city": created_airport_info["city"],
        "country": created_airport_info["country"]
    }

    response = admin_api_client.put(
        endpoint=f"/airports/{iata_code_to_update}",
        json_data=update_payload
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "String should match pattern '^[A-Z]{3}$'"


def test_update_airport_with_valid_iata_code(api_client, admin_token, created_airport_info):
    """
    Verifica que la API acepta una actualización con un código IATA de 3 letras.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    iata_code_to_update = created_airport_info["iata_code"]

    fake = Faker()
    update_payload = {
        "iata_code": "NEW",
        "city": fake.city(),
        "country": fake.country()
    }

    response = admin_api_client.put(
        endpoint=f"/airports/{iata_code_to_update}",
        json_data=update_payload
    )

    assert response.status_code == 200

def test_update_airport_with_non_string_country(api_client, admin_token, airport_payload):
    """
    Verifica que la API rechace una actualización con un país que no sea un string.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    creation_response = admin_api_client.post(endpoint="/airports", data=airport_payload)
    assert creation_response.status_code == 201
    iata_code_to_update = airport_payload["iata_code"]

    update_payload = {
        "iata_code": iata_code_to_update,
        "city": airport_payload["city"],
        "country": 12345,  # Un número
    }
    response = admin_api_client.put(endpoint=f"/airports/{iata_code_to_update}", json_data=update_payload)
    assert response.status_code == 422
    assert "Input should be a valid string" in response.json()["detail"][0]["msg"]







