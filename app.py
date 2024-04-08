# Importamos las librerías necesarias para la aplicación web. el archivo por defecto debe llamarse app.apy para q
# para que funcione,si quieres cambiar el nombre,lo tienes que aclarar en el cmd
from flask import Flask, request, jsonify, render_template
import re  # Librería para trabajar con expresiones regulares.
import secrets  # Librería para generar contraseñas seguras.
import string  # Librería que contiene secuencias de caracteres comunes.

# Inicializamos nuestra aplicación Flask.
app = Flask(__name__)

# Creamos un diccionario para almacenar los usuarios y sus contraseñas.
users = {}

# Establecemos los requisitos para las contraseñas.
password_requirements = {
    'uppercase': 1,  # Al menos 1 letra mayúscula.
    'digits': 1,     # Al menos 1 dígito.
    'special': 1,    # Al menos 1 carácter especial.
    'min_length': 8  # Longitud mínima de 8 caracteres.
}

# Definimos una función para verificar si una contraseña cumple con los requisitos.
def check_password_requirements(password):
    # Verificamos la presencia de letras mayúsculas.
    has_uppercase = len(re.findall(r'[A-Z]', password)) >= password_requirements['uppercase']
    # Verificamos la presencia de dígitos.
    has_digit = len(re.findall(r'\d', password)) >= password_requirements['digits']
    # Verificamos la presencia de caracteres especiales.
    has_special = len(re.findall(r'\W', password)) >= password_requirements['special']
    # Verificamos la longitud de la contraseña.
    is_long_enough = len(password) >= password_requirements['min_length']
    # La contraseña es válida si cumple con todos los requisitos.
    return has_uppercase and has_digit and has_special and is_long_enough

# Definimos una función para generar una contraseña segura.
def generate_secure_password():
    # Creamos un alfabeto que incluye letras, dígitos y signos de puntuación.
    alphabet = string.ascii_letters + string.digits + string.punctuation
    # Generamos una contraseña que cumpla con los requisitos.
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(password_requirements['min_length']))
        if check_password_requirements(password):
            break
    return password

# Definimos una ruta para generar contraseñas seguras.
@app.route('/generate-password', methods=['POST'])
def generate_password():
    # Devolvemos una contraseña segura en formato JSON.
    return jsonify({'password': generate_secure_password()})

# Definimos una ruta para el registro de usuarios.
@app.route('/register', methods=['POST'])
def register():
    # Obtenemos el nombre y la contraseña del formulario.
    name = request.form['name']
    password = request.form['password']

    # Verificamos los requisitos de la contraseña.
    if not check_password_requirements(password):
        # Si no cumple, devolvemos un error.
        return jsonify({'error': 'La contraseña debe tener al menos 8 caracteres, incluyendo mayúsculas, minúsculas, caracter especiales y números.'}), 400

    # Verificamos si el usuario ya existe.
    if name in users:
        # Si existe, devolvemos un error.
        return jsonify({'error': 'El usuario ya existe'}), 400

    # Registramos al usuario.
    users[name] = {'password': password}
    # Devolvemos un mensaje de éxito.
    return jsonify({'message': 'Usuario registrado con éxito'})

# Definimos una ruta para el inicio de sesión de usuarios.
@app.route('/login', methods=['POST'])
def login():
    # Obtenemos el nombre de usuario y la contraseña del formulario.
    username = request.form['username']
    password = request.form['password']

    # Verificamos si el usuario está registrado.
    if username not in users:
        # Si no está registrado, devolvemos un error.
        return jsonify({'error': 'Usuario no registrado'}), 400

    # Verificamos si la contraseña es correcta.
    if users[username]['password'] != password:
        # Si la contraseña es incorrecta, devolvemos un error.
        return jsonify({'error': 'Contraseña errónea, intente otra vez'}), 400

    # Si todo es correcto, damos la bienvenida al usuario.
    return jsonify({'message': 'Bienvenido, ' + username})

# Definimos la ruta principal que carga la página de inicio.
@app.route('/')
def index():
    # Renderizamos la plantilla HTML para la página de inicio.
    return render_template('index.html')

# Verificamos si el script se ejecuta como programa principal.
if __name__ == '__main__':
    # Ejecutamos la aplicación en modo de depuración.
    app.run(debug=True)
