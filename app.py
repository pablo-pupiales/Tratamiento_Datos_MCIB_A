#Archivo con el codigo para la API 

# Archivo con el codigo para la API
# Este archivo crea un microservicio (una API) usando Flask.
# Una API permite que otras aplicaciones se comuniquen con este programa por medio de URLs.
# Por ejemplo, podrás enviar números a una ruta y recibir su suma o multiplicación en formato JSON.

from flask import Flask, jsonify, request # Importa librería flask que tiene modulos Flask,jsonofiy etc
# Flask es la envoltura que nos permite generar la app
# jsonify para dar formato json
# request para hacer request http

# A partir de aquí se crea una instancia de la aplicación Flask (nuestro servidor web).
app = Flask(__name__) # Inicializa la aplicación de tipo Flask

# A continuación se definen "rutas" o "endpoints": direcciones URL a las que el cliente puede llamar.

@app.route('/') # Ruta principal
# Lo que sigue es la función que se ejecuta cuando alguien visita la ruta '/' (la raíz del servidor).
def home():
    # jsonify convierte un diccionario de Python en una respuesta JSON entendible por el cliente.
    # Devuelve un mensaje de bienvenida en formato JSON.
    return jsonify({'message': 'Bienvenido a la API de Microservicio Base - Tratamiento de Datos Paralelo A'})

@app.route('/api/sumar', methods=['POST']) # Endpoint para sumar dos números
# Esta función responde cuando se hace una solicitud POST a /api/sumar.
# Se espera que el cliente envíe un JSON con dos valores: 'a' y 'b'.
def sumar():
    # request.get_json() lee el cuerpo (body) de la solicitud asumiendo que viene en formato JSON.
    data = request.get_json()
    # Extraemos los valores 'a' y 'b' del JSON recibido.
    a = data.get('a')
    b = data.get('b')
    # Validación: si 'a' o 'b' no vienen en el JSON, se devuelve un error 400 (petición incorrecta).
    if a is None or b is None:
        return jsonify({'error': 'Parámetros a y b requeridos'}), 400
    # Si todo está bien, responde con la suma. Ojo: si 'a' y 'b' no son números, Python podría concatenar (si fueran strings).
    # En un sistema real, convendría convertir a int/float y validar tipos, pero aquí respetamos el código original.
    return jsonify({'resultado': a + b})

@app.route('/api/multiplicar', methods=['POST']) # Endpoint para multiplicar dos números
# Esta función responde a /api/multiplicar y espera un JSON con 'a' y 'b', igual que el anterior.
def multiplicar():
    # Leemos el JSON enviado por el cliente.
    data = request.get_json()
    # Obtenemos 'a' y 'b' del JSON. Si no existen, .get devolverá None.
    a = data.get('a')
    b = data.get('b')
    # Validación básica: si falta alguno, se indica error al cliente con código 400.
    if a is None or b is None:
        return jsonify({'error': 'Parámetros a y b requeridos'}), 400
    # Devuelve el producto de 'a' por 'b'.
    # Igual que antes, aquí se asume que 'a' y 'b' son numéricos (no hay conversión explícita).
    return jsonify({'resultado': a * b})

@app.route('/api/info', methods=['GET']) # Endpoint para obtener información del microservicio
# Esta ruta sirve para consultar metadatos del servicio (nombre, versión, descripción, autor).
# Es útil para verificar que el servicio está activo y conocer su versión.
def info():
    # Devuelve un diccionario con información del microservicio convertido a JSON.
    return jsonify({
        'nombre': 'Microservicio Base - Tratamiento de Datos Paralelo A',
        'version': '1.0.0',
        'descripcion': 'Este microservicio realiza operaciones básicas de suma y proporciona información del servicio.',
        'autor': 'Carlos Vintimilla',
    })


# Este bloque se ejecuta solo cuando el archivo se ejecuta directamente (no cuando se importa desde otro módulo).
if __name__ == '__main__':  # Ejecuta la aplicación Flask
    # app.run inicia el servidor web.
    # debug=True: recarga automática al guardar cambios y muestra errores detallados en el navegador (útil en desarrollo).
    # host='0.0.0.0': permite que la app sea accesible desde otras máquinas de la misma red (no solo desde tu PC).
    # port=8080: el puerto donde estará escuchando el servidor. La URL local sería http://localhost:8080/
    app.run(debug=True, host='0.0.0.0', port=8080) # Permite que la aplicación sea accesible desde cualquier IP en el puerto 8080