import pytest
from api.utils.api_client import APIClient
from faker import Faker

# ----------------- Pruebas Create Payment -----------------

def test_create_payment_as_admin_successfully(auth_api_client, payment_payload):
    """
    Verifica que un usuario admin puede crear un pago con éxito usando el fixture de payload.
    """
    response = auth_api_client.post(endpoint="/payments", data=payment_payload)

    assert response.status_code == 201

    response_data = response.json()

    assert "id" in response_data
    assert response_data["booking_id"] == payment_payload["booking_id"]
    assert response_data["status"] == "pending"


def test_create_payment_as_passenger_successfully(api_client, created_passenger_user_info,
                                                  payment_payload_as_passenger):
    """
    Verifica que un usuario 'passenger' puede crear un pago para su propia reserva.
    """
    passenger_api_client = APIClient(base_url=api_client.base_url, token=created_passenger_user_info["token"])

    response = passenger_api_client.post(endpoint="/payments", data=payment_payload_as_passenger)

    assert response.status_code == 201

    response_data = response.json()
    assert "id" in response_data
    assert response_data["booking_id"] == payment_payload_as_passenger["booking_id"]
    assert response_data["status"] == "pending"


def test_create_payment_fails_without_token(api_client, payment_payload):
    """
    Verifica que la API rechace la petición si no se envía ningún token.
    """
    unauth_api_client = APIClient(base_url=api_client.base_url)
    response = unauth_api_client.post(endpoint="/payments", data=payment_payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

# ----------------- Pruebas Get Payment -----------------

def test_get_payment_fails_without_token(api_client):
    """
    Verifica que un usuario no autenticado no puede obtener un pago por ID.
    """
    fake = Faker()
    payment_id = "pym-" + fake.uuid4()

    unauth_api_client = APIClient(base_url=api_client.base_url)
    response = unauth_api_client.get(endpoint=f"/payments/{payment_id}")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_get_payment_with_non_existent_id(auth_api_client):
    """
    Verifica que la API devuelva 404 si el ID del pago no existe.
    """
    fake = Faker()
    non_existent_id = "pym-" + fake.uuid4()
    response = auth_api_client.get(endpoint=f"/payments/{non_existent_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"
