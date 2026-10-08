from config import settings

def test_obtener_libros_vacio(client):
    response = client.get("/libros/")
    assert response.status_code == 200
    assert response.json() == []

def test_crear_libro_sin_api_key(client):
    # Intentar crear un libro sin incluir la cabecera x-api-key debe fallar con 401
    payload = {"titulo": "Libro de Prueba", "autor": "Autor Test"}
    response = client.post("/libros/", json=payload)
    assert response.status_code in (401, 422)

def test_crear_libro_con_api_key(client):
    # Crear un libro con la API Key válida
    headers = {"x-api-key": settings.api_key}
    payload = {"titulo": "Cien años de soledad", "autor": "Gabriel García Márquez"}
    response = client.post("/libros/", json=payload, headers=headers)
    
    assert response.status_code == 201
    datos = response.json()
    assert datos["titulo"] == payload["titulo"]
    assert datos["autor"] == payload["autor"]
    assert "id" in datos

def test_paginacion_y_busqueda(client):
    headers = {"x-api-key": settings.api_key}
    
    # Insertar dos libros de prueba
    client.post("/libros/", json={"titulo": "Python 101", "autor": "Guido"}, headers=headers)
    client.post("/libros/", json={"titulo": "FastAPI Avanzado", "autor": "Tiangolo"}, headers=headers)

    # Probar filtro por búsqueda
    response = client.get("/libros/?buscar=Python")
    assert response.status_code == 200
    libros = response.json()
    assert len(libros) == 1
    assert libros[0]["titulo"] == "Python 101"

    # Probar paginación
    response_paginado = client.get("/libros/?limit=1")
    assert response_paginado.status_code == 200
    assert len(response_paginado.json()) == 1