import pytest
from faker import Faker
from api.utils.api_client import APIClient

# ----------------- Pruebas Create Booking -----------------

def test_create_booking_as_admin_successfully(auth_api_client, created_flight, booking_payload):
    """
    Verifica que un usuario admin puede crear una reserva con éxito.
    """
    response = auth_api_client.post(endpoint="/bookings", data=booking_payload)
    assert response.status_code == 201

    response_data = response.json()
    assert "id" in response_data
    assert response_data["flight_id"] == booking_payload["flight_id"]
    assert response_data["passengers"][0]["full_name"] == booking_payload["passengers"][0]["full_name"]


def test_create_booking_as_passenger_successfully(api_client, created_passenger_user_info, created_flight,
                                                  booking_payload):
    """
    Verifica que un usuario 'passenger' puede crear una reserva con éxito.
    """
    passenger_api_client = APIClient(base_url=api_client.base_url, token=created_passenger_user_info["token"])

    response = passenger_api_client.post(endpoint="/bookings", data=booking_payload)
    assert response.status_code == 201

    response_data = response.json()
    assert "id" in response_data
    assert response_data["flight_id"] == booking_payload["flight_id"]
    assert response_data["user_id"] == created_passenger_user_info["id"]

def test_create_booking_fails_without_token(api_client, created_flight, booking_payload):
    """
    Verifica que la API rechace la petición si no se envía ningún token.
    """
    unauth_api_client = APIClient(base_url=api_client.base_url)

    response = unauth_api_client.post(endpoint="/bookings", data=booking_payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

# ----------------- Pruebas Get Booking -----------------

def test_get_bookings_with_admin_token(api_client, created_booking, admin_token):
    """
    Verifica que un usuario admin puede acceder a la lista de reservas.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)

    params = {"skip": 0, "limit": 1}
    response = admin_api_client.get(endpoint="/bookings", params=params)

    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 1


def test_get_bookings_with_passenger_token(api_client, created_booking, created_passenger_user_info):
    """
    Verifica que un usuario 'passenger' puede acceder a reservas.
    """
    # 1. Crear un cliente de API autenticado como el passenger
    passenger_api_client = APIClient(base_url=api_client.base_url, token=created_passenger_user_info["token"])

    # 2. Crear una reserva con el token del passenger
    booking_payload = {
        "flight_id": created_booking["flight_id"],
        "passengers": [{"full_name": "Test Passenger", "passport": "12345", "seat": "10A"}]
    }
    booking_response = passenger_api_client.post(endpoint="/bookings", data=booking_payload)
    assert booking_response.status_code == 201

    # 3. Listar las reservas del passenger
    params = {"skip": 0, "limit": 1}
    response = passenger_api_client.get(endpoint="/bookings", params=params)

    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 1

    # 4. Validar que la reserva listada pertenece al passenger
    assert response_data[0]["user_id"] == created_passenger_user_info["id"]


def test_get_bookings_without_token(api_client):
    """
    Verifica que la API rechace la petición si no se envía ningún token.
    """
    unauth_api_client = APIClient(base_url=api_client.base_url)

    response = unauth_api_client.get(endpoint="/bookings")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_get_bookings_according_pagination(api_client, created_booking, admin_token):
    """
    Verifica que la paginación de la búsqueda funciona correctamente.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)

    params = {"skip": 1, "limit": 2}
    response = admin_api_client.get(endpoint="/bookings", params=params)

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 2
    assert isinstance(response_data, list)

# ----------------- Pruebas Get Booking por ID-----------------

def test_get_booking_by_id_with_admin_token(api_client, created_booking, admin_token):
    """
    Verifica que un usuario 'admin' puede acceder a cualquier reserva por su ID.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)

    booking_id = created_booking["id"]
    response = admin_api_client.get(endpoint=f"/bookings/{booking_id}")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == booking_id
    assert "flight_id" in response_data
    assert "user_id" in response_data


def test_get_booking_by_id_with_passenger_token(api_client, created_booking, created_passenger_user_info):
    """
    Verifica que un usuario 'passenger' puede obtener su propia reserva por ID.
    """

    # 1. Crear un cliente de API para el passenger
    passenger_client = APIClient(base_url=api_client.base_url, token=created_passenger_user_info["token"])

    # 2. El passenger crea su propia reserva
    booking_payload = {
        "flight_id": created_booking["flight_id"],
        "passengers": [{"full_name": "Test Passenger", "passport": "12345", "seat": "10A"}]
    }
    booking_response = passenger_client.post(endpoint="/bookings", data=booking_payload)
    assert booking_response.status_code == 201
    booking_id_passenger = booking_response.json()["id"]

    # 3. El passenger accede a su propia reserva por ID
    response = passenger_client.get(endpoint=f"/bookings/{booking_id_passenger}")
    assert response.status_code == 200
    assert response.json()["id"] == booking_id_passenger


def test_get_booking_by_id_without_token(api_client, created_booking):
    """
    Verifica que un usuario no autenticado no puede obtener una reserva por ID.
    """
    unauth_api_client = APIClient(base_url=api_client.base_url)
    booking_id = created_booking["id"]

    response = unauth_api_client.get(endpoint=f"/bookings/{booking_id}")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_passenger_cannot_get_other_user_booking(api_client, created_booking, created_passenger_user_info):
    """
    Verifica que un 'passenger' no puede obtener la reserva de otro usuario.
    """
    booking_id_admin = created_booking["id"]
    passenger_api_client = APIClient(base_url=api_client.base_url, token=created_passenger_user_info["token"])

    response = passenger_api_client.get(endpoint=f"/bookings/{booking_id_admin}")

    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"

# ----------------- Pruebas Patch Booking por ID-----------------

def test_admin_can_patch_booking_successfully(api_client, admin_token, created_booking):
    """
    Verifica que un usuario 'admin' puede actualizar una reserva.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    booking_id_to_patch = created_booking["id"]

    # Payload para la actualización
    patch_payload = {
        "additionalProp1": {}
    }

    # Acción: Enviar la petición PATCH
    patch_response = admin_api_client.patch(endpoint=f"/bookings/{booking_id_to_patch}", json_data=patch_payload)

    # Validar la respuesta
    assert patch_response.status_code == 200
    assert patch_response.json()["id"] == booking_id_to_patch

    # La respuesta debería contener los datos originales
    assert patch_response.json()["flight_id"] == created_booking["flight_id"]


def test_passenger_can_patch_own_booking_successfully(api_client, created_passenger_user_info,
                                                      created_booking_as_passenger):
    """
    Verifica que un 'passenger' puede actualizar su propia reserva.
    """
    booking_id = created_booking_as_passenger["id"]

    # 1. Usar el fixture correcto para obtener el token del pasajero.
    passenger_client = APIClient(base_url=api_client.base_url, token=created_passenger_user_info["token"])

    # 2. El resto del test permanece igual.
    patch_payload = {
        "additionalProp1": {}
    }

    patch_response = passenger_client.patch(endpoint=f"/bookings/{booking_id}", json_data=patch_payload)

    assert patch_response.status_code == 200
    assert patch_response.json()["id"] == booking_id

def test_patch_booking_fails_with_non_draft_status(api_client, admin_token, created_booking):
    """
    Verifica que la API rechace la actualización si el estado de la reserva no es 'draft'.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)

    # Primer intento: pasa de draft a ready (actualmente da 500, debería ser 200 o 204)
    admin_api_client.patch(
        endpoint=f"/bookings/{created_booking['id']}",
        json_data={"status": "ready"}
    )

    # Segundo intento: ya no está en draft, debería dar 400
    patch_response = admin_api_client.patch(
        endpoint=f"/bookings/{created_booking['id']}",
        json_data={"status": "confirmed"}
    )

    assert patch_response.status_code == 400
    assert patch_response.json()["detail"] == "Only draft bookings can be edited"



def test_patch_booking_fails_with_passenger_token(api_client, admin_token, created_booking,
                                                  created_passenger_user_info):
    """
    Verifica que la API rechace la petición si el token de un 'passenger' intenta actualizar la reserva de otro.
    """
    booking_id_to_patch = created_booking["id"]

    passenger_api_client = APIClient(base_url=api_client.base_url, token=created_passenger_user_info["token"])
    patch_payload = {"additionalProp1": {}}
    patch_response = passenger_api_client.patch(endpoint=f"/bookings/{booking_id_to_patch}", json_data=patch_payload)

    assert patch_response.status_code == 403
    assert patch_response.json()["detail"] == "Forbidden"

def test_patch_booking_fails_without_token(api_client, admin_token, created_booking):
    """
    Verifica que la API rechace la petición si no se envía ningún token.
    """
    booking_id_to_patch = created_booking["id"]

    unauth_api_client = APIClient(base_url=api_client.base_url)
    patch_payload = {"additionalProp1": {}}
    patch_response = unauth_api_client.patch(endpoint=f"/bookings/{booking_id_to_patch}", json_data=patch_payload)

    assert patch_response.status_code == 401
    assert patch_response.json()["detail"] == "Not authenticated"

# ----------------- Pruebas Delete Booking por ID-----------------

def test_delete_booking_with_admin_token(api_client, created_booking, admin_token):
    """
    Verifica que un usuario 'admin' puede eliminar cualquier reserva por su ID.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    booking_id_to_delete = created_booking["id"]

    response = admin_api_client.delete(endpoint=f"/bookings/{booking_id_to_delete}")

    assert response.status_code == 204
    assert not response.content  # El cuerpo debe estar vacío para un 204

def test_delete_booking_with_passenger_token(api_client, created_booking_as_passenger, created_passenger_user_info):
    """
    Verifica que un usuario 'passenger' puede eliminar su propia reserva por ID.
    """
    booking_id_to_delete = created_booking_as_passenger["id"]

    # Crea el cliente del API con el token del usuario pasajero
    passenger_api_client = APIClient(base_url=api_client.base_url, token=created_passenger_user_info["token"])

    # Ahora el test puede proceder
    response = passenger_api_client.delete(endpoint=f"/bookings/{booking_id_to_delete}")

    assert response.status_code == 204
    assert not response.content


def test_delete_booking_without_token(api_client, created_booking):
    """
    Verifica que un usuario no autenticado no puede eliminar una reserva por ID.
    """
    unauth_api_client = APIClient(base_url=api_client.base_url)
    booking_id_to_delete = created_booking["id"]

    response = unauth_api_client.delete(endpoint=f"/bookings/{booking_id_to_delete}")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_delete_booking_fails_with_non_existent_id(api_client, admin_token):
    """
    Verifica que la API devuelva 404 Not Found si el ID de la reserva no existe.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    non_existent_id = "bkg-xxxxxxxxxxxx"

    response = admin_api_client.delete(endpoint=f"/bookings/{non_existent_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"