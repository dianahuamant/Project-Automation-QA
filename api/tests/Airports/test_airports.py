import pytest
from faker import Faker
from api.utils.api_client import APIClient
import requests

# ----------------- Pruebas para Create Airport -----------------

def test_create_airport_successfully_with_admin_token(api_client, admin_token, airport_payload):
    """
    Verifica que un usuario admin puede crear un aeropuerto con éxito.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)

    response = admin_api_client.post(endpoint="/airports", data=airport_payload)

    assert response.status_code == 201

    response_data = response.json()
    assert response_data["iata_code"] == airport_payload["iata_code"]
    assert response_data["city"] == airport_payload["city"]
    assert response_data["country"] == airport_payload["country"]

def test_create_airport_fails_with_passenger_token(api_client, created_passenger_user_info, airport_payload):
    """
    Verifica que un usuario 'passenger' no puede crear un aeropuerto.
    """
    user_api_client = APIClient(base_url=api_client.base_url, token=created_passenger_user_info["token"])

    response = user_api_client.post(endpoint="/airports", data=airport_payload)

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin privileges required"


def test_create_airport_fails_without_token(api_client, airport_payload):
    """
    Verifica que la API rechace la petición si no se envía ningún token.
    """
    unauth_api_client = APIClient(base_url=api_client.base_url)

    response = unauth_api_client.post(endpoint="/airports", data=airport_payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

# ----------------- Pruebas para Get Airport -----------------

def test_get_airports_successfully(api_client):
    """
    Verifica que se puede obtener la lista de aeropuertos sin autenticación.
    """
    params = {"skip": 0, "limit": 3}
    response = api_client.get(endpoint="/airports", params=params)

    assert response.status_code == 200

    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 3

    # Validar el schema de un aeropuerto en la lista
    assert "iata_code" in response_data[0]
    assert "city" in response_data[0]
    assert "country" in response_data[0]


def test_get_airports_according_pagination(api_client):
    """
    Verifica que la paginación es de acuerdo con 'skip' y 'limit'.
    """
    params = {"skip": 1, "limit": 2}
    response = api_client.get(endpoint="/airports", params=params)

    assert response.status_code == 200

    response_data = response.json()
    assert len(response_data) == 2
    assert isinstance(response_data, list)

# ----------------- Pruebas para Listar aeropuertos según IATA CODE -----------------

def test_get_airport_successfully(api_client, created_airport_info):
    """
    Verifica que se puede obtener la información de un aeropuerto previamente creado.
    """
    iata_code = created_airport_info["iata_code"]

    response = api_client.get(endpoint=f"/airports/{iata_code}")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["iata_code"] == iata_code
    assert response_data["city"] == created_airport_info["city"]
    assert response_data["country"] == created_airport_info["country"]

def test_get_airport_with_non_existent_iata_code(api_client):
    """
    Verifica que la API devuelva 404 Not Found si el aeropuerto no existe.
    """
    non_existent_iata_code = "DYZ"
    response = api_client.get(endpoint=f"/airports/{non_existent_iata_code}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"

# ----------------- Pruebas para Update Airport -----------------

def test_admin_can_update_airport_successfully(api_client, admin_token, created_airport_info):
    """
    Verifica que un usuario admin puede actualizar un aeropuerto con éxito.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    iata_code_to_update = created_airport_info["iata_code"]

    # Crear payload de actualización
    from faker import Faker
    fake = Faker()
    update_payload = {
        "iata_code": iata_code_to_update,  # no cambiamos el IATA
        "city": fake.city(),
        "country": fake.country()
    }

    # Actualizar aeropuerto
    update_response = admin_api_client.put(endpoint=f"/airports/{iata_code_to_update}", json_data=update_payload)
    assert update_response.status_code == 200

    # Validar la respuesta
    response_data = update_response.json()
    assert response_data["iata_code"] == update_payload["iata_code"]
    assert response_data["city"] == update_payload["city"]
    assert response_data["country"] == update_payload["country"]

def test_update_airport_fails_with_passenger_token(api_client, signup_payload, created_passenger_user_info, admin_token, airport_payload):
    """
    Verifica que un usuario 'passenger' no puede actualizar un aeropuerto.
    """
    # Precondición: Crear un aeropuerto
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    creation_response = admin_api_client.post(endpoint="/airports", data=airport_payload)
    assert creation_response.status_code == 201
    iata_code_to_update = airport_payload["iata_code"]

    # Acción: Intentar actualizar con un token de passenger
    user_api_client = APIClient(base_url=api_client.base_url, token=created_passenger_user_info["token"])

    update_payload = {"city": "New City"}
    update_response = user_api_client.put(endpoint=f"/airports/{iata_code_to_update}", json_data=update_payload)

    # Validar el error
    assert update_response.status_code == 403
    assert update_response.json()["detail"] == "Admin privileges required"


def test_update_airport_fails_without_token(api_client, airport_payload, admin_token):
    """
    Verifica que la API rechace la petición si no se envía ningún token.
    """
    # Precondición: Crear un aeropuerto
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    creation_response = admin_api_client.post(endpoint="/airports", data=airport_payload)
    assert creation_response.status_code == 201
    iata_code_to_update = airport_payload["iata_code"]

    # Acción: Intentar actualizar sin token
    unauth_api_client = APIClient(base_url=api_client.base_url)
    update_payload = {"city": "New City"}
    update_response = unauth_api_client.put(endpoint=f"/airports/{iata_code_to_update}", json_data=update_payload)

    # Validar el error
    assert update_response.status_code == 401
    assert update_response.json()["detail"] == "Not authenticated"

# ----------------- Pruebas para Delete Airport -----------------

def test_admin_can_delete_airport_successfully(api_client, admin_token, created_airport_info):
    """
    Verifica que un usuario 'admin' puede eliminar un aeropuerto con éxito.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)

    iata_code_to_delete = created_airport_info["iata_code"]

    # Acción: Eliminar el aeropuerto
    delete_response = admin_api_client.delete(f"/airports/{iata_code_to_delete}")

    # Validaciones
    assert delete_response.status_code == 204
    assert not delete_response.content


def test_passenger_cannot_delete_airport(api_client, created_passenger_user_info, admin_token, airport_payload):
    """
    Verifica que un usuario 'passenger' no puede eliminar un aeropuerto.
    """
    # Precondición: Crear un aeropuerto
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    creation_response = admin_api_client.post(endpoint="/airports", data=airport_payload)
    assert creation_response.status_code == 201

    iata_code_to_delete = airport_payload["iata_code"]

    # Acción: Intentar eliminar con un token de passenger
    passenger_api_client = APIClient(base_url=api_client.base_url, token=created_passenger_user_info["token"])
    delete_response = passenger_api_client.delete(f"/airports/{iata_code_to_delete}")

    # Validar el error
    assert delete_response.status_code == 403
    assert delete_response.json()["detail"] == "Admin privileges required"


def test_delete_airport_fails_without_token(api_client, admin_token, airport_payload):
    """
    Verifica que la API rechace la petición si no se envía ningún token.
    """
    # Precondición: Crear un aeropuerto
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    creation_response = admin_api_client.post(endpoint="/airports", data=airport_payload)
    assert creation_response.status_code == 201

    iata_code_to_delete = airport_payload["iata_code"]

    # Acción: Intentar eliminar sin token
    unauth_api_client = APIClient(base_url=api_client.base_url)
    delete_response = unauth_api_client.delete(f"/airports/{iata_code_to_delete}")

    # Validar el error
    assert delete_response.status_code == 401
    assert delete_response.json()["detail"] == "Not authenticated"

