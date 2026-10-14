def test_crear_libro_con_autenticacion(client):
    # 1. Registramos un usuario
    client.post(
        "/auth/registro",
        json={"email": "autor@correo.com", "password": "securepassword"},
    )

    # 2. Iniciamos sesión para obtener el token de acceso
    response_login = client.post(
        "/auth/login",
        data={"username": "autor@correo.com", "password": "securepassword"},
    )
    assert response_login.status_code == 200
    token = response_login.json()["access_token"]

    # 3. Intentamos crear un libro enviando el token en los headers
    headers = {"Authorization": f"Bearer {token}"}
    response_libro = client.post(
        "/libros/",
        json={"titulo": "Clean Code", "autor": "Robert C. Martin"},
        headers=headers,
    )
    assert response_libro.status_code == 201
    data_libro = response_libro.json()
    assert data_libro["titulo"] == "Clean Code"
    assert data_libro["autor"] == "Robert C. Martin"