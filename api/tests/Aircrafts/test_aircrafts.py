import pytest
from faker import Faker
from api.utils.api_client import APIClient
import requests

# ----------------- Pruebas de Create Aircraft -----------------

def test_create_aircraft_successfully_with_admin_token(api_client, admin_token, aircraft_payload):
    """
    Verifica que un usuario admin puede crear una aeronave con éxito.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)

    response = admin_api_client.post(endpoint="/aircrafts", data=aircraft_payload)

    assert response.status_code == 201

    response_data = response.json()
    assert response_data["tail_number"] == aircraft_payload["tail_number"]
    assert response_data["model"] == aircraft_payload["model"]
    assert response_data["capacity"] == aircraft_payload["capacity"]
    assert "id" in response_data

def test_create_aircraft_fails_with_passenger_token(api_client, created_passenger_user_info, aircraft_payload):
    """
    Verifica que un usuario 'passenger' no puede crear una aeronave.
    """
    user_api_client = APIClient(base_url=api_client.base_url, token=created_passenger_user_info["token"])

    response = user_api_client.post(endpoint="/aircrafts", data=aircraft_payload)

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin privileges required"


def test_create_aircraft_fails_without_token(api_client, aircraft_payload):
    """
    Verifica que la API rechace la petición si no se envía ningún token.
    """
    unauth_api_client = APIClient(base_url=api_client.base_url)

    response = unauth_api_client.post(endpoint="/aircrafts", data=aircraft_payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

# ----------------- Pruebas de Get Aircraft -----------------

def test_get_aircrafts_successfully(api_client, created_aircraft_list):
    """
    Verifica que se puede obtener la lista de aeronaves sin autenticación
    y que existan al menos 2 aeronaves creadas previamente.
    """
    params = {"skip": 0, "limit": 3}
    response = api_client.get(endpoint="/aircrafts", params=params)

    assert response.status_code == 200
    data = response.json()

    # Deben devolverse 3 aeronaves
    assert len(data) == 3
    assert isinstance(data, list)


def test_get_aircrafts_according_pagination(api_client):
    """
    Verifica que la paginación con 'skip' y 'limit' funciona correctamente.
    """
    params = {"skip": 1, "limit": 2}
    response = api_client.get(endpoint="/aircrafts", params=params)

    assert response.status_code == 200

    response_data = response.json()
    assert len(response_data) == 2
    assert isinstance(response_data, list)

# ----------------- Pruebas de Get Aircraft por ID-----------------

def test_get_aircraft_by_id_successfully(api_client, admin_token, aircraft_payload):
    """
    Verifica que se puede obtener la información de una aeronave previamente creada.
    """
    # Precondición: Crear una aeronave para poder buscarla
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    creation_response = admin_api_client.post(endpoint="/aircrafts", data=aircraft_payload)
    assert creation_response.status_code == 201

    aircraft_id = creation_response.json()["id"]

    # Acción: Buscar la aeronave por su ID
    response = api_client.get(endpoint=f"/aircrafts/{aircraft_id}")

    # Validaciones
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == aircraft_id
    assert response_data["tail_number"] == aircraft_payload["tail_number"]
    assert response_data["model"] == aircraft_payload["model"]
    assert response_data["capacity"] == aircraft_payload["capacity"]

def test_get_aircraft_with_non_existent_id(api_client):
    """
    Verifica que la API devuelva 404 Not Found si el ID no existe.
    """
    non_existent_id = "acf-xxxxxxxxxxxx"  # Un ID con formato válido, pero que no está en la base de datos
    response = api_client.get(endpoint=f"/aircrafts/{non_existent_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"

# ----------------- Pruebas para Actualizar Aircraft-----------------

def test_admin_can_update_aircraft_successfully(api_client, admin_token, aircraft_payload):
    """
    Verifica que un usuario admin puede actualizar una aeronave con éxito.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    creation_response = admin_api_client.post(endpoint="/aircrafts", data=aircraft_payload)
    assert creation_response.status_code == 201
    aircraft_id_to_update = creation_response.json()["id"]

    fake = Faker()
    update_payload = {
        "tail_number": fake.unique.lexify(text="??????").upper(),
        "model": fake.word(),
        "capacity": fake.random_int(min=1, max=200)
    }

    update_response = admin_api_client.put(endpoint=f"/aircrafts/{aircraft_id_to_update}", json_data=update_payload)
    assert update_response.status_code == 200

    response_data = update_response.json()
    assert response_data["id"] == aircraft_id_to_update
    assert response_data["tail_number"] == update_payload["tail_number"]
    assert response_data["model"] == update_payload["model"]


def test_update_aircraft_fails_with_passenger_token(api_client, admin_token, aircraft_payload,
                                                    created_passenger_user_info):
    """
    Verifica que un usuario 'passenger' no puede actualizar una aeronave.
    """
    # Precondición: Crear una aeronave
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    creation_response = admin_api_client.post(endpoint="/aircrafts", data=aircraft_payload)
    assert creation_response.status_code == 201
    aircraft_id_to_update = creation_response.json()["id"]

    # Acción: Intentar actualizar con un token de passenger
    user_api_client = APIClient(base_url=api_client.base_url, token=created_passenger_user_info["token"])

    update_payload = {"model": "New Model", "tail_number": "TAIL123", "capacity": 100}
    update_response = user_api_client.put(endpoint=f"/aircrafts/{aircraft_id_to_update}", json_data=update_payload)

    assert update_response.status_code == 403
    assert update_response.json()["detail"] == "Admin privileges required"


def test_update_aircraft_fails_without_token(api_client, admin_token, aircraft_payload):
    """
    Verifica que la API rechace la petición si no se envía ningún token.
    """
    # Precondición: Crear una aeronave
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    creation_response = admin_api_client.post(endpoint="/aircrafts", data=aircraft_payload)
    assert creation_response.status_code == 201
    aircraft_id_to_update = creation_response.json()["id"]

    # Acción: Intentar actualizar sin token
    unauth_api_client = APIClient(base_url=api_client.base_url)
    update_payload = {"model": "New Model", "tail_number": "TAIL123", "capacity": 100}
    update_response = unauth_api_client.put(endpoint=f"/aircrafts/{aircraft_id_to_update}", json_data=update_payload)

    assert update_response.status_code == 401
    assert update_response.json()["detail"] == "Not authenticated"

# ----------------- Pruebas para Delete Aircraft-----------------

def test_admin_can_delete_aircraft_successfully(api_client, admin_token, aircraft_payload):
    """
    Verifica que un usuario 'admin' puede eliminar una aeronave con éxito.
    """
    # Precondición: Crear una aeronave para poder eliminarla
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    creation_response = admin_api_client.post(endpoint="/aircrafts", data=aircraft_payload)
    assert creation_response.status_code == 201

    aircraft_id_to_delete = creation_response.json()["id"]

    # Acción: Eliminar la aeronave
    delete_response = admin_api_client.delete(f"/aircrafts/{aircraft_id_to_delete}")

    # Validaciones
    assert delete_response.status_code == 204
    assert not delete_response.content  # El cuerpo de la respuesta debe estar vacío

def test_passenger_cannot_delete_aircraft(api_client, created_passenger_user_info, created_aircraft_info):
    """
    Verifica que un usuario 'passenger' no puede eliminar una aeronave.
    """
    # Precondición: aeronave creada con fixture
    aircraft_id_to_delete = created_aircraft_info["id"]

    # Acción: Intentar eliminar con un token de passenger
    passenger_api_client = APIClient(base_url=api_client.base_url, token=created_passenger_user_info["token"])
    delete_response = passenger_api_client.delete(f"/aircrafts/{aircraft_id_to_delete}")

    # Validar el error
    assert delete_response.status_code == 403
    assert delete_response.json()["detail"] == "Admin privileges required"

def test_delete_aircraft_fails_without_token(api_client, admin_token, aircraft_payload):
    """
    Verifica que la API rechace la petición si no se envía ningún token.
    """
    # Precondición: Crear una aeronave
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    creation_response = admin_api_client.post(endpoint="/aircrafts", data=aircraft_payload)
    assert creation_response.status_code == 201

    aircraft_id_to_delete = creation_response.json()["id"]

    # Acción: Intentar eliminar sin token
    unauth_api_client = APIClient(base_url=api_client.base_url)
    delete_response = unauth_api_client.delete(f"/aircrafts/{aircraft_id_to_delete}")

    # Validar el error
    assert delete_response.status_code == 401
    assert delete_response.json()["detail"] == "Not authenticated"