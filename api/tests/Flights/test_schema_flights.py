import pytest
import datetime
from faker import Faker
from api.utils.api_client import APIClient

# ----------------- Pruebas Create Flight-----------------

def test_create_flight_with_valid_data(auth_api_client, flight_payload):
    """
    Verifica que la creación de un vuelo con datos válidos es exitosa.
    """
    response = auth_api_client.post(endpoint="/flights", data=flight_payload)
    assert response.status_code == 201


def test_create_flight_with_invalid_origin_iata_code_format(auth_api_client, flight_payload):
    """
    Verifica que la API rechace un código IATA con formato incorrecto en origin.
    """
    flight_payload["origin"] = "ABCD"
    response = auth_api_client.post(endpoint="/flights", data=flight_payload)
    assert response.status_code == 422
    assert "String should match pattern '^[A-Z]{3}$'" in response.json()["detail"][0]["msg"]

def test_create_flight_with_invalid_destination_iata_code_format(auth_api_client, flight_payload):
    """
    Verifica que la API rechace un código IATA con formato incorrecto en destination.
    """
    flight_payload["destination"] = "ABCD"
    response = auth_api_client.post(endpoint="/flights", data=flight_payload)
    assert response.status_code == 422
    assert "String should match pattern '^[A-Z]{3}$'" in response.json()["detail"][0]["msg"]

def test_create_flight_with_invalid_date_format_departure_time(auth_api_client, flight_payload):
    """
    Verifica que la API rechace un formato de fecha incorrecto en departure time.
    """
    flight_payload["departure_time"] = "not-a-date"
    response = auth_api_client.post(endpoint="/flights", data=flight_payload)
    assert response.status_code == 422
    assert "Input should be a valid datetime" in response.json()["detail"][0]["msg"]

def test_create_flight_with_invalid_date_format_arrival_time(auth_api_client, flight_payload):
    """
    Verifica que la API rechace un formato de fecha incorrecto en arrival_time.
    """
    flight_payload["arrival_time"] = "not-a-date"
    response = auth_api_client.post(endpoint="/flights", data=flight_payload)
    assert response.status_code == 422
    assert "Input should be a valid datetime" in response.json()["detail"][0]["msg"]


def test_create_flight_with_non_numeric_price(auth_api_client, flight_payload):
    """
    Verifica que la API rechace un precio que no sea un número.
    """
    flight_payload["base_price"] = "ten"
    response = auth_api_client.post(endpoint="/flights", data=flight_payload)
    assert response.status_code == 422
    assert "Input should be a valid number, unable to parse string as a number" in response.json()["detail"][0]["msg"]

def test_create_flight_with_negative_price(auth_api_client, flight_payload):
    """
    Verifica que la API rechace la creación de un vuelo si el precio es negativo.
    """
    flight_payload["base_price"] = -50
    response = auth_api_client.post(endpoint="/flights", data=flight_payload)
    assert response.status_code == 422

def test_create_flight_with_non_existent_aircraft_id(auth_api_client, flight_payload):
    """
    Verifica que la API rechace la creación de un vuelo si el aircraft_id no existe.
    """
    fake = Faker()
    flight_payload["aircraft_id"] = "acf-" + fake.uuid4()
    response = auth_api_client.post(endpoint="/flights", data=flight_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Aircraft not found"

def test_create_flight_with_non_existent_airport_returns_404(auth_api_client, flight_payload):
    """
    Verifica que la API rechace la creación de un vuelo si el aeropuerto de origen no existe.
    """
    fake = Faker()
    flight_payload["origin"] = fake.unique.lexify(text="???").upper()
    response = auth_api_client.post(endpoint="/flights", data=flight_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Airport not found"

def test_create_flight_with_non_existent_destination_returns_404(auth_api_client, flight_payload):
    """
    Verifica que la API rechace la creación de un vuelo si el aeropuerto de destino no existe.
    """
    fake = Faker()
    flight_payload["destination"] = fake.unique.lexify(text="???").upper()
    response = auth_api_client.post(endpoint="/flights", data=flight_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Airport not found"

def test_create_flight_with_arrival_before_departure_returns_404(auth_api_client, flight_payload):
    """
    Verifica que la API rechace la creación de un vuelo si la hora de llegada es anterior
    a la de salida.
    """
    departure = datetime.datetime.fromisoformat(flight_payload["departure_time"])
    arrival = departure - datetime.timedelta(hours=1)
    flight_payload["arrival_time"] = arrival.isoformat()
    response = auth_api_client.post(endpoint="/flights", data=flight_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Arrival time must be after departure time"

# ----------------- Pruebas Search Flight-----------------
def test_search_flights_with_invalid_origin_length(api_client, flight_payload):
    flight_payload["origin"] = "BOGOTA"
    params = {"origin": flight_payload["origin"], "destination": flight_payload["destination"], "date": "2025-09-05"}
    response = api_client.get(endpoint="/flights", params=params)
    assert response.status_code == 422
    assert "String should have at most 3 characters" in response.json()["detail"][0]["msg"]


def test_search_flights_with_invalid_destination_length(api_client, flight_payload):
    flight_payload["destination"] = "BOGOTA"
    params = {"origin": flight_payload["origin"], "destination": flight_payload["destination"], "date": "2025-09-05"}
    response = api_client.get(endpoint="/flights", params=params)
    assert response.status_code == 422
    assert "String should have at most 3 characters" in response.json()["detail"][0]["msg"]


def test_search_flights_with_invalid_date_format(api_client, flight_payload):
    params = {"origin": "BOG", "destination": "BOG", "date": "2025-09-05_INVALID"}
    response = api_client.get(endpoint="/flights", params=params)
    assert response.status_code == 422
    assert "Input should be a valid date" in response.json()["detail"][0]["msg"]


def test_search_flights_with_non_integer_skip(api_client):
    params = {"skip": "abc", "limit": 1}
    response = api_client.get(endpoint="/flights", params=params)
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "int_parsing"


def test_search_flights_with_negative_skip(api_client):
    params = {"skip": -1, "limit": 10}
    response = api_client.get(endpoint="/flights", params=params)
    assert response.status_code == 422

def test_search_flights_with_negative_limit(api_client):
    params = {"skip": 0, "limit": -1}
    response = api_client.get(endpoint="/flights", params=params)
    assert response.status_code == 422


def test_search_flights_with_limit_equal_to_zero(api_client):
    params = {"skip": 0, "limit": 0}
    response = api_client.get(endpoint="/flights", params=params)
    assert response.status_code == 200
    assert response.json() == []


def test_search_flights_with_skip_equal_to_zero(api_client):
    params = {"skip": 0, "limit": 1}
    response = api_client.get(endpoint="/flights", params=params)
    assert response.status_code == 200
    assert len(response.json()) == 1

# ----------------- Pruebas Get Flight por ID-----------------

def test_get_flight_with_non_existent_id(api_client):
    """
    Verifica que la API devuelva 404 Not Found si el ID del vuelo no existe.
    """
    non_existent_id = "flt-xxxxxxxxxxxx"  # Un ID con formato válido, pero que no está en la base de datos
    response = api_client.get(endpoint=f"/flights/{non_existent_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"


def test_get_flight_with_invalid_id_format(api_client):
    """
    Verifica que la API devuelva 404 Not Found si el ID tiene un formato incorrecto (ej. un número).
    """
    invalid_id = "123"  # Un ID con formato inválido
    response = api_client.get(endpoint=f"/flights/{invalid_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"

# ----------------- Pruebas Update Flight por ID-----------------

def test_update_flight_with_invalid_origin_iata_code_format(auth_api_client, created_flight):
    """
    Verifica que la API rechace una actualización si el 'origin' no es un código IATA válido.
    """
    flight_id_to_update = created_flight["id"]

    update_payload = created_flight.copy()
    update_payload["origin"] = "ABCD"
    response = auth_api_client.put(endpoint=f"/flights/{flight_id_to_update}", json_data=update_payload)

    assert response.status_code == 422
    assert "String should match pattern '^[A-Z]{3}$'" in response.json()["detail"][0]["msg"]


def test_update_flight_with_invalid_destination_iata_code_format(auth_api_client, created_flight):
    """
    Verifica que la API rechace una actualización si el 'destination' no es un código IATA válido.
    """
    flight_id_to_update = created_flight["id"]
    update_payload = created_flight.copy()
    update_payload["destination"] = "ABCD"
    response = auth_api_client.put(endpoint=f"/flights/{flight_id_to_update}", json_data=update_payload)
    assert response.status_code == 422
    assert "String should match pattern '^[A-Z]{3}$'" in response.json()["detail"][0]["msg"]


def test_update_flight_with_invalid_date_format_departure_time(auth_api_client, created_flight):
    """
    Verifica que la API rechace una actualización con un formato de fecha incorrecto en departure_time.
    """
    flight_id_to_update = created_flight["id"]
    update_payload = created_flight.copy()
    update_payload["departure_time"] = "not-a-date"
    response = auth_api_client.put(endpoint=f"/flights/{flight_id_to_update}", json_data=update_payload)
    assert response.status_code == 422
    assert "Input should be a valid datetime" in response.json()["detail"][0]["msg"]


def test_update_flight_with_invalid_date_format_arrival_time(auth_api_client, created_flight):
    """
    Verifica que la API rechace una actualización con un formato de fecha incorrecto en arrival_time.
    """
    flight_id_to_update = created_flight["id"]
    update_payload = created_flight.copy()
    update_payload["arrival_time"] = "not-a-date"
    response = auth_api_client.put(endpoint=f"/flights/{flight_id_to_update}", json_data=update_payload)
    assert response.status_code == 422
    assert "Input should be a valid datetime" in response.json()["detail"][0]["msg"]


def test_update_flight_with_non_numeric_price(auth_api_client, created_flight):
    """
    Verifica que la API rechace una actualización con un precio que no sea un número.
    """
    flight_id_to_update = created_flight["id"]
    update_payload = created_flight.copy()
    update_payload["base_price"] = "ten"
    response = auth_api_client.put(endpoint=f"/flights/{flight_id_to_update}", json_data=update_payload)
    assert response.status_code == 422
    assert "Input should be a valid number" in response.json()["detail"][0]["msg"]


def test_update_flight_with_negative_price(auth_api_client, created_flight):
    """
    Verifica que la API rechace una actualización si el precio es negativo.
    """
    flight_id_to_update = created_flight["id"]
    update_payload = created_flight.copy()
    update_payload["base_price"] = -50
    response = auth_api_client.put(endpoint=f"/flights/{flight_id_to_update}", json_data=update_payload)
    assert response.status_code == 422

def test_update_flight_with_non_existent_aircraft_id(auth_api_client, created_flight):
    """
    Verifica que la API rechace la actualización si el aircraft_id no existe.
    """
    flight_id_to_update = created_flight["id"]
    fake = Faker()
    update_payload = created_flight.copy()
    update_payload["aircraft_id"] = "acf-" + fake.uuid4()
    response = auth_api_client.put(endpoint=f"/flights/{flight_id_to_update}", json_data=update_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Aircraft not found"


def test_update_flight_with_non_existent_airport_returns_404(auth_api_client, created_flight):
    """
    Verifica que la API rechace la actualización si el aeropuerto de origen no existe.
    """
    flight_id_to_update = created_flight["id"]
    fake = Faker()
    update_payload = created_flight.copy()
    update_payload["origin"] = fake.unique.lexify(text="???").upper()
    response = auth_api_client.put(endpoint=f"/flights/{flight_id_to_update}", json_data=update_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Airport not found"


def test_update_flight_with_non_existent_destination_returns_404(auth_api_client, created_flight):
    """
    Verifica que la API rechace la actualización si el aeropuerto de destino no existe.
    """
    flight_id_to_update = created_flight["id"]
    fake = Faker()
    update_payload = created_flight.copy()
    update_payload["destination"] = fake.unique.lexify(text="???").upper()
    response = auth_api_client.put(endpoint=f"/flights/{flight_id_to_update}", json_data=update_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Airport not found"


def test_update_flight_with_arrival_before_departure_returns_404(auth_api_client, created_flight):
    """
    Verifica que la API rechace una actualización si la hora de llegada es anterior
    a la de salida.
    """
    flight_id_to_update = created_flight["id"]
    departure = datetime.datetime.fromisoformat(created_flight["departure_time"])
    arrival = departure - datetime.timedelta(hours=1)
    update_payload = created_flight.copy()
    update_payload["arrival_time"] = arrival.isoformat()
    response = auth_api_client.put(endpoint=f"/flights/{flight_id_to_update}", json_data=update_payload)
    assert response.status_code == 404