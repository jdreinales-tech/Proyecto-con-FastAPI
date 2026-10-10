def test_registrar_usuario(client):
    response = client.post(
        "/auth/registro",
        json={"email": "testing@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testing@example.com"
    assert "id" in data
    assert "password" not in data  # Verificar que la contraseña no se devuelva


def test_login_usuario(client):
    # 1. Registrar un usuario primero
    client.post(
        "/auth/registro",
        json={"email": "testing@example.com", "password": "password123"}
    )

    # 2. Intentar hacer login con x-www-form-urlencoded
    response = client.post(
        "/auth/login",
        data={"username": "testing@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"