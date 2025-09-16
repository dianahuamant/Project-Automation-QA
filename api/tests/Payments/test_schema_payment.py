import pytest
from faker import Faker
from api.utils.api_client import APIClient

# ----------------- Pruebas Create Payment -----------------

def test_create_payment_with_int_booking_id(auth_api_client, created_booking):
    """
    Verifica que la API rechace la petición si el 'booking_id' es un entero.
    """
    fake = Faker()
    payment_payload = {
        "booking_id": 12345,
        "amount": fake.pyfloat(left_digits=3, right_digits=2, min_value=0),
        "payment_method": fake.credit_card_provider()
    }
    response = auth_api_client.post(endpoint="/payments", data=payment_payload)

    assert response.status_code == 422
    assert "Input should be a valid string" in response.json()["detail"][0]["msg"]


def test_create_payment_with_non_existent_booking_id(auth_api_client):
    """
    Verifica que la API devuelva 404 si el 'booking_id' no existe en la base de datos.
    """
    fake = Faker()
    payment_payload = {
        "booking_id": "bkg-" + fake.uuid4(),
        "amount": fake.pyfloat(left_digits=3, right_digits=2, min_value=0),
        "payment_method": fake.credit_card_provider()
    }

    response = auth_api_client.post(endpoint="/payments", data=payment_payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Booking not found"


def test_create_payment_with_negative_amount(auth_api_client, created_booking):
    """
    Verifica que la API rechace la petición si el 'amount' es un número negativo.
    """
    fake = Faker()
    payment_payload = {
        "booking_id": created_booking["id"],
        "amount": -100,
        "payment_method": fake.credit_card_provider()
    }
    response = auth_api_client.post(endpoint="/payments", data=payment_payload)

    assert response.status_code == 422


def test_create_payment_with_non_string_payment_method(auth_api_client, created_booking):
    """
    Verifica que la API rechace la petición si el 'payment_method' no es un string.
    """
    payment_payload = {
        "booking_id": created_booking["id"],
        "amount": 100,
        "payment_method": 12345  # Valor no string
    }
    response = auth_api_client.post(endpoint="/payments", data=payment_payload)

    assert response.status_code == 422
    assert "Input should be a valid string" in response.json()["detail"][0]["msg"]
