import urllib.request
import json
import time

URL_BASE = "http://localhost:8000"

def probar_api_libros():
    # ---------------------------------------------------------
    # 1. READ (GET): Consultar todos los libros iniciales
    # ---------------------------------------------------------
    print("\n--- 1. CONSULTANDO LIBROS (GET) ---")
    peticion_get = urllib.request.Request(f"{URL_BASE}/libros", method="GET")
    with urllib.request.urlopen(peticion_get) as resp:
        print("Respuesta:", json.loads(resp.read().decode("utf-8")))

    time.sleep(1)

    # ---------------------------------------------------------
    # 2. CREATE (POST): Agregar un nuevo libro
    # ---------------------------------------------------------
    print("\n--- 2. AGREGANDO NUEVO LIBRO (POST) ---")
    nuevo_libro = {
        "titulo": "Cien años de soledad",
        "autor": "Gabriel García Márquez"
    }
    datos_post = json.dumps(nuevo_libro).encode("utf-8")
    
    peticion_post = urllib.request.Request(
        f"{URL_BASE}/libros",
        data=datos_post,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(peticion_post) as resp:
        print("Respuesta:", json.loads(resp.read().decode("utf-8")))

    time.sleep(1)

    # ---------------------------------------------------------
    # 3. UPDATE (PATCH): Prestar un libro (por ejemplo, ID 1)
    # ---------------------------------------------------------
    print("\n--- 3. MARCANDO LIBRO COMO PRESTADO (PATCH) ---")
    datos_patch = json.dumps({"id": 1}).encode("utf-8")
    
    peticion_patch = urllib.request.Request(
        f"{URL_BASE}/libros/1/prestar",
        method="PATCH"
    )
    with urllib.request.urlopen(peticion_patch) as respuesta:
        datos= json.loads(respuesta.read().decode("utf-8"))
        print("Respuesta PATCH", datos)

    time.sleep(1)

    # ---------------------------------------------------------
    # 4. DELETE (DELETE): Eliminar un libro (por ejemplo, ID 2)
    # ---------------------------------------------------------
    print("\n--- 4. ELIMINANDO LIBRO (DELETE) ---")
    datos_delete = json.dumps({"id": 2}).encode("utf-8")
    
    peticion_delete = urllib.request.Request(
        f"{URL_BASE}/libros/2",
        method="DELETE"
    )
    with urllib.request.urlopen(peticion_delete) as respuesta:
        datos= json.loads(respuesta.read().decode("utf-8"))
        print("Respuesta DELETE", datos)
    time.sleep(1)

    # ---------------------------------------------------------
    # 5. READ (GET): Comprobar el estado final de la lista
    # ---------------------------------------------------------
    print("\n--- 5. ESTADO FINAL DE LA BIBLIOTECA (GET) ---")
    peticion_final = urllib.request.Request(f"{URL_BASE}/libros", method="GET")
    with urllib.request.urlopen(peticion_final) as resp:
        print("Respuesta:", json.loads(resp.read().decode("utf-8")))

if __name__ == "__main__":
    try:
        probar_api_libros()
    except Exception as e:
        print(f"\n Ocurrió un error al ejecutar la prueba: {e}")