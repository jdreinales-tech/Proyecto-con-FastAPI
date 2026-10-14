def test_registrar_usuario(client):
    response = client.post(
        "/auth/registro",
        json={"email": "test@correo.com", "password": "123password"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@correo.com"
    assert "id" in data