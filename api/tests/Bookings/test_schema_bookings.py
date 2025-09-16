import pytest
from faker import Faker
from api.utils.api_client import APIClient

# ----------------- Pruebas Create Booking -----------------

def test_create_booking_with_non_existent_flight_id(auth_api_client, booking_payload):
    """
    Verifica que la API rechace la creación de una reserva si el flight_id no existe.
    """
    fake = Faker()
    booking_payload["flight_id"] = "flt-" + fake.uuid4()
    response = auth_api_client.post(endpoint="/bookings", data=booking_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Flight not found"

def test_create_booking_with_non_string_full_name(auth_api_client, booking_payload):
    """
    Verifica que la API rechace una reserva si el 'full_name' no es un string.
    """
    booking_payload["passengers"][0]["full_name"] = 12345
    response = auth_api_client.post(endpoint="/bookings", data=booking_payload)
    assert response.status_code == 422
    assert "Input should be a valid string" in response.json()["detail"][0]["msg"]


def test_create_booking_with_non_string_passport(auth_api_client, booking_payload):
    """
    Verifica que la API rechace una reserva si el 'passport' no es un string.
    """
    booking_payload["passengers"][0]["passport"] = 12345
    response = auth_api_client.post(endpoint="/bookings", data=booking_payload)
    assert response.status_code == 422
    assert "Input should be a valid string" in response.json()["detail"][0]["msg"]


def test_create_booking_with_non_string_seat(auth_api_client, booking_payload):
    """
    Verifica que la API rechace una reserva si el 'seat' no es un string.
    """
    booking_payload["passengers"][0]["seat"] = 12345
    response = auth_api_client.post(endpoint="/bookings", data=booking_payload)
    assert response.status_code == 422
    assert "Input should be a valid string" in response.json()["detail"][0]["msg"]

# ----------------- Pruebas Get Booking -----------------

def test_get_bookings_with_non_integer_skip(auth_api_client):
    """
    Verifica que la API rechace una petición con un 'skip' que no es un entero.
    """
    params = {"skip": "abc", "limit": 1}
    response = auth_api_client.get(endpoint="/bookings", params=params)

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "int_parsing"

def test_get_bookings_with_non_integer_limit(auth_api_client):
    """
    Verifica que la API rechace una petición con un 'limit' que no es un entero.
    """
    params = {"skip": 0, "limit": "abc"}
    response = auth_api_client.get(endpoint="/bookings", params=params)

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "int_parsing"


def test_get_bookings_with_negative_skip(auth_api_client):
    """
    Verifica que la API rechace una petición con un 'skip' negativo.
    """
    params = {"skip": -1, "limit": 10}
    response = auth_api_client.get(endpoint="/bookings", params=params)

    assert response.status_code == 422


def test_get_bookings_with_negative_limit(auth_api_client):
    """
    Verifica que la API rechace una petición con un 'limit' negativo.
    """
    params = {"skip": 0, "limit": -1}
    response = auth_api_client.get(endpoint="/bookings", params=params)

    assert response.status_code == 422

def test_get_bookings_with_limit_equal_to_zero(auth_api_client):
    """
    Verifica que la API devuelva una lista vacía con 'limit=0'.
    """
    params = {"skip": 0, "limit": 0}
    response = auth_api_client.get(endpoint="/bookings", params=params)

    assert response.status_code == 200
    assert response.json() == []


def test_get_bookings_with_skip_equal_to_zero(auth_api_client):
    """
    Verifica que la API acepte 'skip=0' y devuelva resultados.
    """
    params = {"skip": 0, "limit": 1}
    response = auth_api_client.get(endpoint="/bookings", params=params)

    assert response.status_code == 200
    assert len(response.json()) == 1

# ----------------- Pruebas Get Booking por ID-----------------

def test_get_booking_with_non_existent_id(api_client, admin_token):
    """
    Verifica que la API devuelve 404 Not Found si el ID de la reserva no existe.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    non_existent_id = "bkg-xxxxxxxxxxxx"
    response = admin_api_client.get(endpoint=f"/bookings/{non_existent_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"


def test_get_booking_with_invalid_id_format(api_client, admin_token):
    """
    Verifica que la API devuelve 404 Not Found si el ID tiene un formato incorrecto.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    invalid_id = "123"
    response = admin_api_client.get(endpoint=f"/bookings/{invalid_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"



