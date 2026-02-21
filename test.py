import requests
# Importa la librería 'requests', que sirve para hacer solicitudes HTTP (GET, POST, etc.)
# La usaremos para conectarnos a tu API Flask que corre en localhost:8080


def request_info():
    # Define una función que consulta el endpoint GET /api/info de tu API
    url = 'http://localhost:8080/api/info'  # URL del endpoint de información
    response = requests.get(url)            # Realiza una solicitud HTTP GET a esa URL
    return response.json()                  # Convierte la respuesta (JSON) a un dict de Python y lo devuelve


def request_sumar(a, b):
    # Define una función que llama al endpoint POST /api/sumar para sumar dos números
    url = 'http://localhost:8080/api/sumar'  # URL del endpoint de suma
    data = {
        'a': a,  # Primer número que quieres sumar (parámetro 'a' del API)
        'b': b   # Segundo número que quieres sumar (parámetro 'b' del API)
        }
    # Envía una solicitud HTTP POST con el cuerpo en formato JSON.
    # 'json=data' hace que 'requests' serialice 'data' a JSON y ponga el header Content-Type: application/json
    response = requests.post(url, json=data)
    # La API, si todo va bien, responde con un JSON como: {"resultado": 15}
    return response.json()  # Devuelve ese JSON ya convertido en dict de Python


# Llamamos a la función 'request_sumar' enviando 5 y 10 como argumentos.
# Esto hará una llamada HTTP POST a tu API en /api/sumar con {"a": 5, "b": 10}
respuesta = request_sumar(5, 10)

# Imprime en pantalla la respuesta que vino del servidor.
# Ojo: 'respuesta' aquí es un diccionario. Por ejemplo: {'resultado': 15}
# Se imprime usando un f-string para incrustar el dict directamente en el texto.
print(f"Resultado de sumar: {respuesta}")