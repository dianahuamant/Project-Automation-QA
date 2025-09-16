import pytest
from faker import Faker
from api.utils.api_client import APIClient
import requests

# ----------------- Pruebas Create Flight-----------------

def test_create_flight_successfully_with_admin_token(api_client, admin_token, created_flight):
    """
    Verifica que un usuario admin puede crear un vuelo con éxito.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    response = admin_api_client.post(endpoint="/flights", data=created_flight)
    assert response.status_code == 201

    response_data = response.json()
    assert "id" in response_data
    assert response_data["origin"] == created_flight["origin"]
    assert response_data["destination"] == created_flight["destination"]
    assert response_data["base_price"] == created_flight["base_price"]

def test_create_flight_fails_with_passenger_token(api_client, created_passenger_user_info, flight_payload):
    """
    Verifica que un usuario 'passenger' no puede crear un vuelo.
    """
    user_api_client = APIClient(base_url=api_client.base_url, token=created_passenger_user_info["token"])
    response = user_api_client.post(endpoint="/flights", data=flight_payload)
    assert response.status_code == 403
    assert response.json()["detail"] == "Admin privileges required"

def test_create_flight_fails_without_token(api_client, flight_payload):
    """
    Verifica que la API rechace la petición si no se envía ningún token.
    """
    unauth_api_client = APIClient(base_url=api_client.base_url)
    response = unauth_api_client.post(endpoint="/flights", data=flight_payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

# ----------------- Pruebas Search Flight-----------------
def test_search_flights_successfully_with_all_params(api_client, created_flight):
    """
    Verifica que la búsqueda de vuelos funciona con todos los parámetros válidos.
    """
    params = {
        "origin": created_flight["origin"],
        "destination": created_flight["destination"],
        "date": created_flight["departure_time"][:10],
        "skip": 0,
        "limit": 10
    }
    response = api_client.get(endpoint="/flights", params=params)
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) > 0


def test_search_flights_with_pagination(api_client, created_flight_list):
    """
    Verifica que la paginación de la búsqueda funciona correctamente.
    """
    params = {"skip": 1, "limit": 2}
    response = api_client.get(endpoint="/flights", params=params)

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 2
    assert isinstance(response_data, list)

# ----------------- Pruebas Get Flight por ID-----------------

def test_get_flight_by_id_successfully(api_client, created_flight):
    """
    Verifica que se puede obtener la información de un vuelo previamente creado.
    """
    # Obtener el ID del vuelo del fixture
    flight_id = created_flight["id"]

    # Acción: Buscar el vuelo por su ID
    response = api_client.get(endpoint=f"/flights/{flight_id}")

    # Validaciones
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == flight_id
    assert response_data["origin"] == created_flight["origin"]
    assert response_data["destination"] == created_flight["destination"]
    assert response_data["base_price"] == created_flight["base_price"]

# ----------------- Pruebas Update Flight por ID-----------------

def test_admin_can_update_flight_successfully(api_client, admin_token, created_flight):
    """
    Verifica que un usuario admin puede actualizar un vuelo con éxito.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    flight_id_to_update = created_flight["id"]

    fake = Faker()
    update_payload = {
        "origin": created_flight["origin"],
        "destination": created_flight["destination"],
        "departure_time": str(fake.date_time_between(start_date="now", end_date="+2d")),
        "arrival_time": str(fake.date_time_between(start_date="now", end_date="+3d")),
        "base_price": fake.random_int(min=50, max=500),
        "aircraft_id": created_flight["aircraft_id"]
    }

    update_response = admin_api_client.put(endpoint=f"/flights/{flight_id_to_update}", json_data=update_payload)
    assert update_response.status_code == 200

    response_data = update_response.json()
    assert response_data["id"] == flight_id_to_update
    assert response_data["base_price"] == update_payload["base_price"]


def test_update_flight_fails_with_passenger_token(api_client, admin_token, created_flight, created_passenger_user_info):
    """
    Verifica que un usuario 'passenger' no puede actualizar un vuelo.
    """
    user_api_client = APIClient(base_url=api_client.base_url, token=created_passenger_user_info["token"])
    flight_id_to_update = created_flight["id"]

    update_payload = {
        "base_price": 600,
        "origin": created_flight["origin"],
        "destination": created_flight["destination"],
        "departure_time": created_flight["departure_time"],
        "arrival_time": created_flight["arrival_time"],
        "aircraft_id": created_flight["aircraft_id"]
    }
    update_response = user_api_client.put(endpoint=f"/flights/{flight_id_to_update}", json_data=update_payload)

    assert update_response.status_code == 403
    assert update_response.json()["detail"] == "Admin privileges required"


def test_update_flight_fails_without_token(api_client, admin_token, created_flight):
    """
    Verifica que la API rechace la petición si no se envía ningún token.
    """
    unauth_api_client = APIClient(base_url=api_client.base_url)
    flight_id_to_update = created_flight["id"]

    update_payload = {
        "base_price": 600,
        "origin": created_flight["origin"],
        "destination": created_flight["destination"],
        "departure_time": created_flight["departure_time"],
        "arrival_time": created_flight["arrival_time"],
        "aircraft_id": created_flight["aircraft_id"]
    }
    update_response = unauth_api_client.put(endpoint=f"/flights/{flight_id_to_update}", json_data=update_payload)

    assert update_response.status_code == 401
    assert update_response.json()["detail"] == "Not authenticated"

# ----------------- Pruebas Delete Flight por ID-----------------

def test_admin_can_delete_flight_successfully(auth_api_client, created_flight):
    """
    Verifica que un usuario 'admin' puede eliminar un vuelo con éxito.
    """
    flight_id_to_delete = created_flight["id"]

    # Acción: Eliminar el vuelo
    delete_response = auth_api_client.delete(f"/flights/{flight_id_to_delete}")

    # Validaciones
    assert delete_response.status_code == 204
    assert not delete_response.content


def test_passenger_cannot_delete_flight(api_client, created_passenger_user_info, created_flight):
    """
    Verifica que un usuario 'passenger' no puede eliminar un vuelo.
    """
    flight_id_to_delete = created_flight["id"]

    # Acción: Intentar eliminar con un token de passenger
    passenger_api_client = APIClient(base_url=api_client.base_url, token=created_passenger_user_info["token"])
    delete_response = passenger_api_client.delete(f"/flights/{flight_id_to_delete}")

    # Validar el error
    assert delete_response.status_code == 403
    assert delete_response.json()["detail"] == "Admin privileges required"


def test_delete_flight_fails_without_token(api_client, created_flight):
    """
    Verifica que la API rechace la petición si no se envía ningún token.
    """
    flight_id_to_delete = created_flight["id"]

    # Acción: Intentar eliminar sin token
    unauth_api_client = APIClient(base_url=api_client.base_url)
    delete_response = unauth_api_client.delete(f"/flights/{flight_id_to_delete}")

    # Validar el error
    assert delete_response.status_code == 401
    assert delete_response.json()["detail"] == "Not authenticated"