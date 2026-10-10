import pytest


@pytest.fixture
def token_usuario_autenticado(client):
    # 1. Registrar usuario de prueba
    client.post(
        "/auth/registro",
        json={"email": "autor@example.com", "password": "password123"}
    )
    # 2. Iniciar sesión para obtener el JWT
    response = client.post(
        "/auth/login",
        data={"username": "autor@example.com", "password": "password123"}
    )
    return response.json()["access_token"]


def test_crear_libro_exitoso(client, token_usuario_autenticado):
    # Enviar la cabecera Authorization con el token JWT
    headers = {"Authorization": f"Bearer {token_usuario_autenticado}"}
    
    response = client.post(
        "/libros/",
        json={"titulo": "Rayuela", "autor": "Julio Cortázar"},
        headers=headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == "Rayuela"
    assert data["autor"] == "Julio Cortázar"
    assert "id" in data
    assert "usuario_id" in data
    assert data["propietario"]["email"] == "autor@example.com"


def test_crear_libro_sin_autenticacion(client):
    # Intentar crear un libro sin enviar la cabecera de autenticación
    response = client.post(
        "/libros/",
        json={"titulo": "Libro Anónimo", "autor": "Sin Autor"}
    )
    # Debe retornar 401 Unauthorized
    assert response.status_code == 401


def test_obtener_lista_libros(client, token_usuario_autenticado):
    # 1. Crear un libro primero
    headers = {"Authorization": f"Bearer {token_usuario_autenticado}"}
    client.post(
        "/libros/",
        json={"titulo": "Ficciones", "autor": "Jorge Luis Borges"},
        headers=headers
    )

    # 2. Consultar la lista
    response = client.get("/libros/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["titulo"] == "Ficciones"