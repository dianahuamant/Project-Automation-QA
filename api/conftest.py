import pytest
import os
from dotenv import load_dotenv, find_dotenv
from faker import Faker
from api.utils.api_client import APIClient
import requests
import datetime
import time
from api.utils import settings

@pytest.fixture(scope="session")
def api_base_url():
    """
    Fixture que carga la URL base de la API del archivo .env.
    """
    return settings.API_BASE_URL

@pytest.fixture(scope="session")
def api_client(api_base_url):
    """
    Fixture que retorna una instancia del cliente de API lista para usar.
    """
    return APIClient(api_base_url)

@pytest.fixture(scope="session")
def faker():
    """Fixture que retorna una instancia de Faker para usar en las pruebas."""
    return Faker()

@pytest.fixture
def signup_payload():
    """
    Fixture que genera y retorna un payload de registro de usuario con datos únicos.
    """
    fake = Faker()
    payload = {
        "email": fake.unique.email(),
        "password": fake.password(length=7),
        "full_name": fake.name()
    }
    return payload

@pytest.fixture
def login_payload(signup_payload):
    """
    Fixture que genera y retorna un payload de login
    a partir de los datos del fixture signup_payload.
    """
    return {
        "username": signup_payload["email"],
        "password": signup_payload["password"],
    }


@pytest.fixture(scope="session")
def admin_token(api_base_url):
    """
    Fixture que hace login con las credenciales de administrador
    y retorna el token de acceso.
    """
    temp_api_client = APIClient(base_url=api_base_url)

    login_payload = {
        "username": settings.ADMIN_EMAIL,
        "password": settings.ADMIN_PASSWORD
    }

    # Login con post_form
    login_response = temp_api_client.post_form(endpoint="/auth/login", data=login_payload)

    assert login_response.status_code == 200

    return login_response.json()["access_token"]

@pytest.fixture (scope="session")
def auth_api_client(api_base_url, admin_token):
    """
    Fixture que retorna una instancia de APIClient
    ya autenticada con el token de administrador.
    """
    return APIClient(base_url=api_base_url, token=admin_token)

@pytest.fixture
def admin_signup_payload():
    """
    Fixture que genera y retorna un payload de registro de usuario con rol de 'admin'.
    """
    fake = Faker()
    payload = {
        "email": fake.email(),
        "password": fake.password(length=7),
        "full_name": fake.name(),
        "role": "admin"
    }
    return payload


@pytest.fixture
def created_admin_user_info(api_client, admin_token, faker):
    """
    Crea un usuario admin a través del endpoint /users y retorna sus datos y su token.
    """
    max_retries = 5
    signup_response = None
    login_response = None

    # 1. Crear el cliente de API con el token de admin
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)

    # 2. Registrar al usuario con lógica de reintento
    for attempt in range(max_retries):
        try:
            # Generamos un payload de registro único para cada intento
            admin_signup_payload = {
                "email": faker.email(),
                "password": faker.password(length=7),
                "full_name": faker.name(),
                "role": "admin"
            }
            response = admin_api_client.post(endpoint="/users", data=admin_signup_payload)
            response.raise_for_status()
            signup_response = response
            break
        except requests.exceptions.HTTPError as err:
            if response is not None and response.status_code in [400, 500] and attempt < max_retries - 1:
                print(f"⚠️ Signup falló con {response.status_code}. Reintentando... ({attempt + 1}/{max_retries})")
                time.sleep(1)
            else:
                pytest.fail(f"Falla crítica: Signup falló después de {max_retries} intentos. Error: {err}")

    # 3. Hacer login con el nuevo usuario 'admin' para obtener su token
    login_payload = {
        "username": admin_signup_payload["email"],
        "password": admin_signup_payload["password"],
    }

    # Lógica de reintento para el login
    for attempt in range(max_retries):
        try:
            login_response = api_client.post_form(endpoint="/auth/login", data=login_payload)
            login_response.raise_for_status()
            break
        except requests.exceptions.HTTPError as err:
            if login_response is not None and login_response.status_code in [400, 500] and attempt < max_retries - 1:
                print(f"⚠️ Login falló con {login_response.status_code}. Reintentando... ({attempt + 1}/{max_retries})")
                time.sleep(1)
            else:
                pytest.fail(f"Falla crítica: Login falló después de {max_retries} intentos. Error: {err}")

    return {
        "id": signup_response.json()["id"],
        "email": signup_response.json()["email"],
        "full_name": signup_response.json()["full_name"],
        "password": admin_signup_payload["password"],
        "token": login_response.json()["access_token"],
        "role": signup_response.json()["role"],
    }


@pytest.fixture
def created_passenger_user_info(api_client, faker):
    """
    Crea un usuario 'passenger' a través del endpoint /auth/signup
    y retorna sus datos y su token.
    """
    max_retries = 5
    signup_response = None

    # 1. Registrar al usuario con lógica de reintento
    for attempt in range(max_retries):
        try:
            # Generamos un payload de registro único para cada intento
            signup_payload = {
                "email": faker.email(),
                "password": faker.password(length=7),
                "full_name": faker.name()
            }
            response = api_client.post(endpoint="/auth/signup", data=signup_payload)
            response.raise_for_status()
            signup_response = response
            break
        except requests.exceptions.HTTPError as err:
            if response.status_code in [400, 500] and attempt < max_retries - 1:
                print(f"⚠️ Signup falló con {response.status_code}. Reintentando... ({attempt + 1}/{max_retries})")
                time.sleep(1)
            else:
                pytest.fail(f"Falla crítica: Signup falló después de {max_retries} intentos. Error: {err}")

    # 2. Hacer login con el nuevo usuario 'passenger' para obtener su token
    login_payload = {
        "username": signup_payload["email"],
        "password": signup_payload["password"],
    }
    login_response = None

    # Lógica de reintento para el login
    for attempt in range(max_retries):
        try:
            login_response = api_client.post_form(endpoint="/auth/login", data=login_payload)
            login_response.raise_for_status()
            break
        except requests.exceptions.HTTPError as err:
            if login_response is not None and login_response.status_code in [400, 500] and attempt < max_retries - 1:
                print(f"⚠️ Login falló con {login_response.status_code}. Reintentando... ({attempt + 1}/{max_retries})")
                time.sleep(1)
            else:
                pytest.fail(f"Falla crítica: Login falló después de {max_retries} intentos. Error: {err}")

    return {
        "id": signup_response.json()["id"],
        "email": signup_response.json()["email"],
        "full_name": signup_response.json()["full_name"],
        "password": signup_payload["password"],
        "token": login_response.json()["access_token"],
        "role": signup_response.json()["role"],
    }

@pytest.fixture
def airport_payload():
    """
    Fixture que genera y retorna un payload de creación de aeropuerto con datos únicos.
    """
    fake = Faker()
    payload = {
        "iata_code": fake.unique.lexify(text="???").upper(),
        "city": fake.city(),
        "country": fake.country()
    }
    return payload


@pytest.fixture
def aircraft_payload(faker):
    """
    Fixture que genera y retorna un payload de creación de aeronave
    con datos válidos y un 'tail_number' con longitud entre 5 y 10.
    """
    random_length = faker.random_int(min=5, max=10)
    template = "?" * random_length

    payload = {
        "tail_number": faker.lexify(text=template).upper(),
        "model": faker.word(),
        "capacity": faker.random_int(min=0)
    }
    return payload

@pytest.fixture(scope="session")
def created_airport_info(api_client, admin_token, faker):
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)

    max_retries = 5
    for attempt in range(max_retries):
        try:
            payload = {
                "iata_code": faker.lexify(text="???").upper(),
                "city": faker.city(),
                "country": faker.country()
            }
            response = admin_api_client.post(endpoint="/airports", data=payload)
            response.raise_for_status()
            return payload
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"⚠️ ERROR: El servidor falló con {response.status_code}. Reintentando...")

@pytest.fixture(scope="session")
def created_aircraft_info(api_client, admin_token):
    """
    Crea una aeronave y retorna su ID.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    fake = Faker()
    payload = {
        "tail_number": fake.unique.lexify(text="?????").upper(),
        "model": fake.word(),
        "capacity": fake.random_int(min=10, max=300)
    }
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = admin_api_client.post(endpoint="/aircrafts", data=payload)
            response.raise_for_status()
            return {"id": response.json()["id"], "payload": payload}
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"⚠️ ERROR: El servidor falló con {response.status_code}. Reintentando... ({attempt + 1}/{max_retries})")
                time.sleep(1)
            else:
                pytest.fail(f"Falla crítica: La API no respondió correctamente después de {max_retries} intentos. El test no puede continuar. Error: {e}")

@pytest.fixture(scope="function")
def created_aircraft_list(api_client, admin_token, faker):
    """
    Crea una lista de aeronaves y retorna sus payloads.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
    fake = Faker()
    max_retries = 5
    num_aircrafts_to_create = 5
    created_aircrafts = []

    for i in range(num_aircrafts_to_create):
        payload = {
            "tail_number": fake.unique.lexify(text="?????").upper(),
            "model": fake.word(),
            "capacity": fake.random_int(min=10, max=300)
        }

        for attempt in range(max_retries):
            try:
                response = admin_api_client.post(endpoint="/aircrafts", data=payload)
                response.raise_for_status()
                created_aircrafts.append(response.json())
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"⚠️ ERROR: Aeronave {i + 1} falló. Reintentando... ({attempt + 1}/{max_retries})")
                    time.sleep(1)
                else:
                    pytest.fail(
                        f"Falla crítica: No se pudo crear la aeronave {i + 1} después de {max_retries} intentos. Error: {e}"
                    )

    return created_aircrafts

@pytest.fixture (scope="function")
def flight_payload(faker, created_airport_info, created_aircraft_info):
    """
    Fixture que genera y retorna un payload de creación de vuelo válido.
    """
    departure_time = faker.date_time_between(start_date="now", end_date="+1d", tzinfo=datetime.timezone.utc)
    arrival_time = faker.date_time_between(start_date=departure_time, end_date="+2d", tzinfo=datetime.timezone.utc)

    payload = {
        "origin": created_airport_info["iata_code"],
        "destination": created_airport_info["iata_code"],
        "departure_time": departure_time.isoformat(),
        "arrival_time": arrival_time.isoformat(),
        "base_price": faker.random_int(min=50, max=500),
        "aircraft_id": created_aircraft_info["id"]
    }
    return payload

@pytest.fixture
def created_flight(auth_api_client, flight_payload):
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = auth_api_client.post(endpoint="/flights", data=flight_payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            # Captura el código de estado de la respuesta
            status_code = err.response.status_code

            # Reintenta SOLO si el error es un problema del servidor (5xx)
            if 500 <= status_code < 600 and attempt < max_retries - 1:
                print(f"⚠️ Petición falló con {status_code}. Reintentando... ({attempt + 1}/{max_retries})")
                time.sleep(1)
            else:
                # Falla la prueba si el error es 4xx o si se agotaron los reintentos
                pytest.fail(f"Falla crítica: La API no respondió correctamente después de {max_retries} intentos. Error: {err}")

@pytest.fixture(scope="function")
def created_flight_list(auth_api_client, flight_payload, faker):
    """
    Crea una lista de vuelos y retorna sus payloads.
    """
    max_retries = 5
    num_flights_to_create = 5
    created_flights_list = []

    for i in range(num_flights_to_create):
        payload = flight_payload.copy()
        payload["base_price"] = faker.random_int(min=50, max=500)

        for attempt in range(max_retries):
            try:
                response = auth_api_client.post(endpoint="/flights", data=payload)
                response.raise_for_status()
                created_flights_list.append(response.json())
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"⚠️ ERROR: Vuelo {i + 1} falló. Reintentando... ({attempt + 1}/{max_retries})")
                    time.sleep(1)
                else:
                    pytest.fail(f"Falla crítica: No se pudo crear el vuelo {i + 1} después de {max_retries} intentos. Error: {e}")

    return created_flights_list

@pytest.fixture
def booking_payload(faker, created_flight):
    """
    Fixture que genera y retorna un payload de reserva válido.
    """
    payload = {
        "flight_id": created_flight["id"],
        "passengers": [
            {
                "full_name": faker.name(),
                "passport": faker.passport_number(),
                "seat": faker.bothify(text="?#")
            }
        ]
    }
    return payload


@pytest.fixture
def created_booking(api_client, admin_token, booking_payload):
    """
    Crea una reserva en la API y retorna la respuesta completa de la creación.
    """
    max_retries = 5
    for attempt in range(max_retries):
        try:
            admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)
            response = admin_api_client.post(endpoint="/bookings", data=booking_payload)

            # 1. Verifica explícitamente el status code.
            if response.status_code == 201:
                return response.json()
            else:
                # 2. Si el código no es 201, levanta una excepción para que el reintento funcione.
                response.raise_for_status()

        except requests.exceptions.HTTPError as err:
            if attempt < max_retries - 1:
                print(f"⚠️ Petición falló con {response.status_code}. Reintentando... ({attempt + 1}/{max_retries})")
                time.sleep(1)
            else:
                pytest.fail(
                    f"Falla crítica: La API no respondió correctamente después de {max_retries} intentos. Error: {err}")
        except Exception as e:
            pytest.fail(f"Ocurrió un error inesperado al crear la reserva: {e}")

@pytest.fixture
def created_booking_as_passenger(api_client, created_passenger_user_info, booking_payload):
    """
    Crea una reserva en la API como un usuario 'passenger' y retorna la respuesta completa de la creación.
    """
    max_retries = 5
    for attempt in range(max_retries):
        try:
            passenger_api_client = APIClient(base_url=api_client.base_url, token=created_passenger_user_info["token"])
            response = passenger_api_client.post(endpoint="/bookings", data=booking_payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            if attempt < max_retries - 1:
                print(f"⚠️ Petición falló con {response.status_code}. Reintentando... ({attempt + 1}/{max_retries})")
                time.sleep(1)
            else:
                pytest.fail(f"Falla crítica: La API no respondió correctamente después de {max_retries} intentos. Error: {err}")


@pytest.fixture
def payment_payload(faker: Faker, created_booking: dict) -> dict:
    """
    Crea y retorna un payload de pago válido.
    """
    amount_decimal = faker.pydecimal(left_digits=3, right_digits=2, min_value=0)
    payload = {
        "booking_id": created_booking["id"],
        "amount": float(amount_decimal),
        "payment_method": faker.credit_card_provider()
    }
    return payload

@pytest.fixture
def payment_payload_as_passenger(faker: Faker, created_booking_as_passenger: dict) -> dict:
    """
    Crea y retorna un payload de pago válido para una reserva de pasajero.
    """
    payload = {
        "booking_id": created_booking_as_passenger["id"],
        "amount": float(faker.pydecimal(left_digits=3, right_digits=2, min_value=0)),
        "payment_method": faker.credit_card_provider()
    }
    return payload
