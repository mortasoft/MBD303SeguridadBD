from flask import Flask, render_template, request, jsonify
import mysql.connector
import os
import time
import re

app = Flask(__name__)

# Configuración de la base de datos
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'db'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'rootpassword'),
    'database': os.getenv('DB_NAME', 'userdb')
}

def get_db_connection():
    """Establece conexión con la base de datos"""
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except mysql.connector.Error as err:
            if attempt < max_retries - 1:
                print(f"Error conectando a la BD (intento {attempt + 1}/{max_retries}): {err}")
                time.sleep(retry_delay)
            else:
                raise

def sanitize_input(input_string):
    """
    Sanitiza la entrada del usuario eliminando caracteres peligrosos
    Esta es una capa adicional de seguridad, pero NO reemplaza las consultas parametrizadas
    """
    if not input_string:
        return ""
    
    # Eliminar caracteres potencialmente peligrosos
    # Permitir solo letras, números, espacios, guiones y guiones bajos
    sanitized = re.sub(r'[^\w\s\-@.]', '', input_string)
    
    # Limitar longitud
    sanitized = sanitized[:100]
    
    return sanitized

def validate_username(username):
    """
    Valida que el username tenga un formato correcto
    """
    if not username:
        return False
    
    # Solo permite letras, números y guiones bajos, entre 3 y 50 caracteres
    pattern = r'^[a-zA-Z0-9_]{3,50}$'
    return bool(re.match(pattern, username))

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/users')
def users():
    """Muestra todos los usuarios"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Consulta segura - sin parámetros de usuario
        query = "SELECT id, username, email FROM users"
        cursor.execute(query)
        
        users_list = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('users.html', users=users_list)
    except Exception as e:
        # No exponer detalles del error al usuario
        print(f"Error interno: {str(e)}")
        return "Error interno del servidor", 500

@app.route('/search')
def search():
    """Búsqueda de usuarios - SEGURA con consultas parametrizadas"""
    username = request.args.get('username', '')
    
    if not username:
        return render_template('search.html', users=None, query='')
    
    # Sanitizar entrada (capa adicional de seguridad)
    username_sanitized = sanitize_input(username)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # ¡SEGURO! - Uso de consultas parametrizadas con placeholders
        # El driver de MySQL se encarga de escapar correctamente los parámetros
        query = "SELECT id, username, email FROM users WHERE username = %s"
        
        print(f"[SECURE] Ejecutando query parametrizada con username: {username_sanitized}")
        
        # Los parámetros se pasan como tupla separada
        cursor.execute(query, (username_sanitized,))
        
        users_list = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('search.html', users=users_list, query=username_sanitized)
    except Exception as e:
        # No exponer detalles del error
        print(f"Error interno: {str(e)}")
        return render_template('search.html', users=None, query=username_sanitized, 
                             error="Error al procesar la búsqueda")

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login de usuarios - SEGURO con consultas parametrizadas"""
    if request.method == 'GET':
        return render_template('login.html')
    
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    # Validar formato de entrada
    if not validate_username(username):
        return render_template('login.html', 
                             error="Formato de usuario inválido. Use solo letras, números y guiones bajos (3-50 caracteres)")
    
    # Sanitizar entrada
    username_sanitized = sanitize_input(username)
    password_sanitized = sanitize_input(password)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # ¡SEGURO! - Consulta parametrizada
        query = "SELECT id, username, email FROM users WHERE username = %s AND password = %s"
        
        print(f"[SECURE] Ejecutando query parametrizada para login de: {username_sanitized}")
        
        # Parámetros pasados de forma segura
        cursor.execute(query, (username_sanitized, password_sanitized))
        
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            return render_template('login.html', success=True, user=user)
        else:
            return render_template('login.html', error="Usuario o contraseña incorrectos")
    except Exception as e:
        print(f"Error interno: {str(e)}")
        return render_template('login.html', error="Error al procesar el login")

@app.route('/api/search')
def api_search():
    """API endpoint para búsqueda - SEGURO"""
    username = request.args.get('username', '')
    
    if not username:
        return jsonify({'error': 'Username parameter required'}), 400
    
    # Sanitizar entrada
    username_sanitized = sanitize_input(username)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # ¡SEGURO! - Consulta parametrizada con LIKE
        # Importante: los wildcards (%) se agregan en el parámetro, no en la query
        query = "SELECT id, username, email FROM users WHERE username LIKE %s"
        
        print(f"[SECURE] Ejecutando query parametrizada con LIKE: {username_sanitized}")
        
        # El parámetro incluye los wildcards de forma segura
        search_param = f"%{username_sanitized}%"
        cursor.execute(query, (search_param,))
        
        users_list = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify({'users': users_list, 'count': len(users_list)})
    except Exception as e:
        print(f"Error interno: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected', 'version': '2.0-secure'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': 'Database connection failed'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
