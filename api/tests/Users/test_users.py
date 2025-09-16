import pytest
import requests
from faker import Faker
from api.utils.api_client import APIClient
from api.utils import settings

# ----------------- Pruebas para Create User as Admin -----------------

def test_create_new_admin_user_with_admin_permissions(api_client, admin_token, signup_payload):
    """
    Verifica que un usuario con permisos de administrador puede crear un nuevo usuario con rol de 'admin'.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)

    payload_to_admin = signup_payload.copy()
    payload_to_admin["role"] = "admin"

    response = admin_api_client.post(endpoint="/users", data=payload_to_admin)

    assert response.status_code == 201

    response_data = response.json()
    assert response_data["email"] == payload_to_admin["email"]
    assert response_data["role"] == "admin"


def test_create_user_fails_with_invalid_token(api_client, signup_payload):
    """
    Verifica que la API rechace una petición con un token inválido.
    """
    invalid_token = "invalid_token_123"
    unauth_api_client = APIClient(base_url=api_client.base_url, token=invalid_token)

    user_payload = signup_payload.copy()
    user_payload["role"] = "passenger"

    response = unauth_api_client.post(endpoint="/users", data=user_payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


def test_create_user_fails_without_any_token(api_client, signup_payload):
    """
    Verifica que la API rechace una petición sin enviar ningún token.
    """
    unauth_api_client = APIClient(base_url=api_client.base_url)

    user_payload = signup_payload.copy()
    user_payload["role"] = "passenger"

    response = unauth_api_client.post(endpoint="/users", data=user_payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_user_fails_with_passenger_token(api_client, signup_payload):
    """
    Verifica que la API rechace una petición con un token de usuario normal (passenger).
    """
    # 1. Registrar a un usuario normal (precondición del test)
    signup_response = api_client.post("/auth/signup", data=signup_payload)
    assert signup_response.status_code == 201

    # 2. Obtener el token del usuario normal
    login_payload = {
        "username": signup_payload["email"],
        "password": signup_payload["password"],
    }

    login_url = f"{api_client.base_url}/auth/login"
    login_response = requests.post(login_url, data=login_payload)
    user_token = login_response.json()["access_token"]

    # 3. Crear una instancia de APIClient con el token del usuario normal
    user_api_client = APIClient(base_url=api_client.base_url, token=user_token)

    # 4. Preparar el payload de un nuevo usuario
    new_user_payload = signup_payload.copy()
    new_user_payload["role"] = "passenger"

    # 5. Enviar la petición con el token de usuario normal
    response = user_api_client.post(endpoint="/users", data=new_user_payload)

    # 6. Validar que la API devuelve un error de autorización
    assert response.status_code == 403
    assert response.json()["detail"] == "Admin privileges required"

# ----------------- Pruebas para List Users -----------------

def test_get_users_successfully(api_client, admin_token):
    """
    Verifica que se puede obtener la lista de usuarios con permisos de admin.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)

    params = {"skip": 0, "limit": 3}
    response = admin_api_client.get(endpoint="/users", params=params)

    assert response.status_code == 200

    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 3

    # Validar el schema de un usuario en la lista
    assert "id" in response_data[0]
    assert "email" in response_data[0]
    assert "full_name" in response_data[0]
    assert "role" in response_data[0]


def test_get_users_according_pagination(api_client, admin_token):
    """
    Verifica que la paginación con 'skip' y 'limit' funciona correctamente.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)

    params = {"skip": 1, "limit": 2}
    response = admin_api_client.get(endpoint="/users", params=params)

    assert response.status_code == 200

    response_data = response.json()
    assert len(response_data) == 2
    assert isinstance(response_data, list)


def test_get_users_fails_with_passenger_token(api_client, created_passenger_user_info):
    """
    Verifica que un usuario 'passenger' no puede acceder a la lista de usuarios.
    """
    user_api_client = APIClient(
        base_url=api_client.base_url,
        token=created_passenger_user_info["token"]
    )

    response = user_api_client.get(endpoint="/users")

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin privileges required"


def test_get_users_without_token(api_client):
    """
    Verifica que la API rechace la petición si no se envía ningún token.
    """
    unauth_api_client = APIClient(base_url=api_client.base_url)

    response = unauth_api_client.get(endpoint="/users")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

# ----------------- Pruebas para List Users -----------------

def test_get_my_user_data_with_admin_token(api_client, admin_token):
    """
    Verifica que el endpoint /users/me devuelve los datos del usuario admin.
    """
    # 1. Crear una instancia de APIClient con el token de admin
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)

    # 2. Enviar la petición GET
    response = admin_api_client.get(endpoint="/users/me")

    # 3. Validar la respuesta
    assert response.status_code == 200
    response_data = response.json()

    # Se validan los datos del usuario admin usando las variables del .env
    assert response_data["email"] == settings.ADMIN_EMAIL  # <-- CAMBIO AQUÍ
    assert response_data["full_name"] == settings.ADMIN_FULL_NAME  # <-- CAMBIO AQUÍ
    assert response_data["role"] == settings.ADMIN_ROLE  # <-- CAMBIO AQUÍ

def test_get_my_user_data_with_passenger_token(api_client, created_passenger_user_info):
    """
    Verifica que un usuario normal puede obtener sus propios datos.
    """
    user_api_client = APIClient(
        base_url=api_client.base_url,
        token=created_passenger_user_info["token"]
    )

    # Enviar la petición GET a /users/me
    response = user_api_client.get(endpoint="/users/me")
    assert response.status_code == 200

    response_data = response.json()

    # Validar que los datos coinciden con el usuario creado por el fixture
    assert response_data["email"] == created_passenger_user_info["email"]
    assert response_data["full_name"] == created_passenger_user_info["full_name"]
    assert response_data["role"] == "passenger"

def test_get_my_user_data_without_token(api_client):
    """
    Verifica que la API rechace la petición si no se envía ningún token.
    """
    # 1. Crear una instancia de APIClient sin token
    unauth_api_client = APIClient(base_url=api_client.base_url)

    # 2. Enviar la petición GET a /users/me
    response = unauth_api_client.get(endpoint="/users/me")

    # 3. Validar el fallo
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

# ----------------- Pruebas para Update Users -----------------

def test_passenger_user_can_successfully_update_password(api_client, created_passenger_user_info):
    """
    Verifica que un usuario puede actualizar su propio password y que la API
    responde con un 200 OK.
    """
    user_id = created_passenger_user_info["id"]
    user_api_client = APIClient(
        base_url=api_client.base_url,
        token=created_passenger_user_info["token"]
    )
    email = created_passenger_user_info["email"]
    full_name = created_passenger_user_info["full_name"]

    # Preparar el payload de actualización con un nuevo password
    from faker import Faker
    fake = Faker()
    new_password = fake.password(length=8)
    update_payload = {
        "email": email,
        "password": new_password,
        "full_name": full_name
    }

    # Enviar la petición PUT
    update_response = user_api_client.put(endpoint=f"/users/{user_id}", json_data=update_payload)

    # Validar que la actualización fue exitosa
    assert update_response.status_code == 200

def test_passenger_login_with_new_password(api_client, created_passenger_user_info):
    """
    Verifica que el password actualizado se puede usar para iniciar sesión.
    """
    user_id = created_passenger_user_info["id"]
    user_api_client = APIClient(base_url=api_client.base_url, token=created_passenger_user_info["token"])
    email = created_passenger_user_info["email"]
    full_name = created_passenger_user_info["full_name"]

    # 1. Actualizar el password
    from faker import Faker
    fake = Faker()
    new_password = fake.password(length=8)
    update_payload = {
        "email": email,
        "password": new_password,
        "full_name": full_name
    }

    update_response = user_api_client.put(endpoint=f"/users/{user_id}", json_data=update_payload)
    assert update_response.status_code == 200

    # 2. Intentar login con el nuevo password
    new_login_payload = {"username": email, "password": new_password}
    new_login_response = api_client.post_form(endpoint="/auth/login", data=new_login_payload)
    assert new_login_response.status_code == 200
    response_data = new_login_response.json()
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"

def test_passenger_user_can_successfully_update_email(api_client, signup_payload):
    """
    Verifica que un usuario puede actualizar su propio email y que el cambio
    se refleja en la API.
    """
    # 1. Registrar a un usuario
    signup_response = api_client.post(endpoint="/auth/signup", data=signup_payload)
    assert signup_response.status_code == 201
    user_id = signup_response.json()["id"]

    # 2. Obtener el token del usuario
    login_payload = {"username": signup_payload["email"], "password": signup_payload["password"]}
    login_response = api_client.post_form(endpoint="/auth/login", data=login_payload)
    user_token = login_response.json()["access_token"]
    user_api_client = APIClient(base_url=api_client.base_url, token=user_token)

    # 3. Preparar el payload de actualización con un nuevo email
    fake = Faker()
    new_email = fake.email()
    update_payload = {
        "email": new_email,
        "password": signup_payload["password"],
        "full_name": signup_payload["full_name"]
    }

    # 4. Enviar la petición PUT
    update_response = user_api_client.put(endpoint=f"/users/{user_id}", json_data=update_payload)
    assert update_response.status_code == 200

    # 5. Verificar que el email actualizado se refleja en /users/me
    me_response = user_api_client.get(endpoint="/users/me")
    assert me_response.status_code == 200
    assert me_response.json()["email"] == new_email

def test_passenger_updated_email_is_reflected_in_me_endpoint(api_client, signup_payload):
    """
    Verifica que el email actualizado se refleja al obtener el usuario con /users/me.
    """
    signup_response = api_client.post(endpoint="/auth/signup", data=signup_payload)
    assert signup_response.status_code == 201
    user_id = signup_response.json()["id"]

    login_payload = {"username": signup_payload["email"], "password": signup_payload["password"]}
    login_response = api_client.post_form(endpoint="/auth/login", data=login_payload)
    user_token = login_response.json()["access_token"]
    user_api_client = APIClient(base_url=api_client.base_url, token=user_token)

    fake = Faker()
    new_email = fake.email()
    update_payload = {
        "email": new_email,
        "password": signup_payload["password"],
        "full_name": signup_payload["full_name"]
    }

    update_response = user_api_client.put(endpoint=f"/users/{user_id}", json_data=update_payload)
    assert update_response.status_code == 200

    me_response = user_api_client.get(endpoint="/users/me")
    assert me_response.status_code == 200
    assert me_response.json()["email"] == new_email

def test_passenger_user_can_successfully_update_full_name(api_client, created_passenger_user_info, faker):
    """
    Verifica que un usuario puede actualizar su nombre completo.
    """
    user_id = created_passenger_user_info["id"]
    user_token = created_passenger_user_info["token"]

    user_api_client = APIClient(base_url=api_client.base_url, token=user_token)

    # Generar un nuevo nombre aleatorio
    new_full_name = faker.name()
    update_payload = {
        "email": created_passenger_user_info["email"],
        "password": created_passenger_user_info["password"],
        "full_name": new_full_name
    }

    update_response = user_api_client.put(endpoint=f"/users/{user_id}", json_data=update_payload)

    assert update_response.status_code == 200
    assert update_response.json()["full_name"] == new_full_name

def test_passenger_updated_full_name_is_reflected_in_me_endpoint(api_client, signup_payload):
    """
    Verifica que el nombre actualizado se refleja al obtener el usuario con /users/me.
    """
    signup_response = api_client.post(endpoint="/auth/signup", data=signup_payload)
    assert signup_response.status_code == 201
    user_id = signup_response.json()["id"]

    login_payload = {"username": signup_payload["email"], "password": signup_payload["password"]}
    login_response = api_client.post_form(endpoint="/auth/login", data=login_payload)
    user_token = login_response.json()["access_token"]
    user_api_client = APIClient(base_url=api_client.base_url, token=user_token)

    fake = Faker()
    new_full_name = fake.name()
    update_payload = {
        "email": signup_payload["email"],
        "password": signup_payload["password"],
        "full_name": new_full_name
    }

    update_response = user_api_client.put(endpoint=f"/users/{user_id}", json_data=update_payload)
    assert update_response.status_code == 200

    me_response = user_api_client.get(endpoint="/users/me")
    assert me_response.status_code == 200
    assert me_response.json()["full_name"] == new_full_name


def test_admin_user_can_successfully_update_password(api_client, created_admin_user_info):
    """
    Verifica que un usuario admin puede actualizar su propio password y que la API
    responde con un 200 OK.
    """
    user_id = created_admin_user_info["id"]
    admin_api_client = APIClient(base_url=api_client.base_url, token=created_admin_user_info["token"])

    fake = Faker()
    new_password = fake.password(length=8)
    update_payload = {
        "email": created_admin_user_info["email"],
        "password": new_password,
        "full_name": created_admin_user_info["full_name"]
    }

    update_response = admin_api_client.put(endpoint=f"/users/{user_id}", json_data=update_payload)
    assert update_response.status_code == 200

def test_admin_login_with_new_password_fails(api_client, created_admin_user_info):
    """
    Verifica el bug de la API donde el login con un password de admin recién actualizado
    falla con un error 500.
    """
    user_id = created_admin_user_info["id"]
    admin_api_client = APIClient(base_url=api_client.base_url, token=created_admin_user_info["token"])

    fake = Faker()
    new_password = fake.password(length=8)
    update_payload = {
        "email": created_admin_user_info["email"],
        "password": new_password,
        "full_name": created_admin_user_info["full_name"]
    }
    update_response = admin_api_client.put(endpoint=f"/users/{user_id}", json_data=update_payload)
    assert update_response.status_code == 200

    new_login_payload = {"username": created_admin_user_info["email"], "password": new_password}
    new_login_response = api_client.post_form(endpoint="/auth/login", data=new_login_payload)
    assert new_login_response.status_code == 500

def test_admin_user_can_successfully_update_email(api_client, created_admin_user_info):
    """
    Verifica que un usuario admin puede actualizar su propio email.
    """
    user_id = created_admin_user_info["id"]
    admin_api_client = APIClient(base_url=api_client.base_url, token=created_admin_user_info["token"])

    fake = Faker()
    new_email = fake.email()
    update_payload = {
        "email": new_email,
        "password": created_admin_user_info["password"],
        "full_name": created_admin_user_info["full_name"]
    }

    update_response = admin_api_client.put(endpoint=f"/users/{user_id}", json_data=update_payload)
    assert update_response.status_code == 200

def test_admin_updated_email_is_reflected_in_me_endpoint(api_client, created_admin_user_info):
    """
    Verifica que el email actualizado de un admin se refleja al obtener el usuario con /users/me.
    """
    user_id = created_admin_user_info["id"]
    admin_api_client = APIClient(base_url=api_client.base_url, token=created_admin_user_info["token"])

    fake = Faker()
    new_email = fake.email()
    update_payload = {
        "email": new_email,
        "password": created_admin_user_info["password"],
        "full_name": created_admin_user_info["full_name"]
    }

    update_response = admin_api_client.put(endpoint=f"/users/{user_id}", json_data=update_payload)
    assert update_response.status_code == 200

    me_response = admin_api_client.get(endpoint="/users/me")
    assert me_response.status_code == 200
    assert me_response.json()["email"] == new_email

def test_admin_user_can_successfully_update_full_name(api_client, created_admin_user_info):
    """
    Verifica que un usuario admin puede actualizar su nombre completo.
    """
    user_id = created_admin_user_info["id"]
    admin_api_client = APIClient(base_url=api_client.base_url, token=created_admin_user_info["token"])

    fake = Faker()
    new_full_name = fake.name()
    update_payload = {
        "email": created_admin_user_info["email"],
        "password": created_admin_user_info["password"],
        "full_name": new_full_name
    }

    update_response = admin_api_client.put(endpoint=f"/users/{user_id}", json_data=update_payload)
    assert update_response.status_code == 200

def test_admin_updated_full_name_is_reflected_in_me_endpoint(api_client, created_admin_user_info):
    """
    Verifica que el nombre actualizado de un admin se refleja al obtener el usuario con /users/me.
    """
    user_id = created_admin_user_info["id"]
    admin_api_client = APIClient(base_url=api_client.base_url, token=created_admin_user_info["token"])

    fake = Faker()
    new_full_name = fake.name()
    update_payload = {
        "email": created_admin_user_info["email"],
        "password": created_admin_user_info["password"],
        "full_name": new_full_name
    }

    update_response = admin_api_client.put(endpoint=f"/users/{user_id}", json_data=update_payload)
    assert update_response.status_code == 200

    me_response = admin_api_client.get(endpoint="/users/me")
    assert me_response.status_code == 200
    assert me_response.json()["full_name"] == new_full_name

# ----------------- Pruebas de Delete User -----------------

def test_delete_user_without_token_returns_401(api_client, created_passenger_user_info):
    """
    Verifica que la petición DELETE sin token de autenticación devuelva 401 Unauthorized.
    """
    user_id_to_delete = created_passenger_user_info["id"]
    response = api_client.delete(f"/users/{user_id_to_delete}")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_passenger_cannot_delete_user_returns_403(api_client, created_passenger_user_info, signup_payload):
    """
    Verifica que un usuario 'passenger' no puede eliminar a otro usuario y devuelve 403 Forbidden.
    """
    passenger_api_client = APIClient(base_url=api_client.base_url, token=created_passenger_user_info["token"])

    # 1. Crear un segundo usuario para intentar eliminarlo
    second_user_payload = signup_payload.copy()
    fake = Faker()
    second_user_payload["email"] = fake.email()

    signup_response = api_client.post(endpoint="/auth/signup", data=second_user_payload)
    assert signup_response.status_code == 201

    user_id_to_delete = signup_response.json()["id"]

    # 2. Intentar eliminar al segundo usuario con el token del primer passenger
    response = passenger_api_client.delete(f"/users/{user_id_to_delete}")

    # 3. Validar el error de permisos
    assert response.status_code == 403
    assert response.json()["detail"] == "Admin privileges required"


def test_admin_can_delete_passenger_user(api_client, created_admin_user_info, created_passenger_user_info):
    """
    Verifica que un usuario 'admin' puede eliminar a un usuario 'passenger' con éxito.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=created_admin_user_info["token"])
    user_id_to_delete = created_passenger_user_info["id"]

    # 1. Eliminar al usuario passenger
    delete_response = admin_api_client.delete(f"/users/{user_id_to_delete}")
    assert delete_response.status_code == 204
    assert not delete_response.content


def test_admin_can_delete_another_admin_user(api_client, admin_token, admin_signup_payload):
    """
    Verifica que un usuario 'admin' puede eliminar a otro usuario 'admin'.
    """
    admin_api_client = APIClient(base_url=api_client.base_url, token=admin_token)

    # 1. Usar el token del admin principal para crear un segundo admin
    signup_response = admin_api_client.post(endpoint="/users", data=admin_signup_payload)
    assert signup_response.status_code == 201

    # 2. Obtener el ID del segundo admin
    user_id_to_delete = signup_response.json()["id"]

    # 3. Eliminar al segundo usuario admin con el token del admin principal
    delete_response = admin_api_client.delete(f"/users/{user_id_to_delete}")
    assert delete_response.status_code == 204
    assert not delete_response.content
