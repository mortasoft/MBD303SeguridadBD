from flask import Flask, render_template, request, jsonify
import mysql.connector
import os
import time

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
        
        # Consulta vulnerable - concatenación directa
        query = "SELECT id, username, email FROM users"
        cursor.execute(query)
        
        users_list = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('users.html', users=users_list)
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/search')
def search():
    """Búsqueda de usuarios - VULNERABLE A SQL INJECTION"""
    username = request.args.get('username', '')
    
    if not username:
        return render_template('search.html', users=None, query='')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # ¡VULNERABLE! - Concatenación directa sin sanitización
        query = f"SELECT id, username, email, password FROM users WHERE username = '{username}'"
        
        print(f"[VULNERABLE] Ejecutando query: {query}")
        cursor.execute(query)
        
        users_list = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('search.html', users=users_list, query=username)
    except Exception as e:
        return render_template('search.html', users=None, query=username, error=str(e))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login de usuarios - VULNERABLE A SQL INJECTION"""
    if request.method == 'GET':
        return render_template('login.html')
    
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # ¡VULNERABLE! - Concatenación directa sin sanitización
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        
        print(f"[VULNERABLE] Ejecutando query: {query}")
        cursor.execute(query)
        
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            return render_template('login.html', success=True, user=user)
        else:
            return render_template('login.html', error="Usuario o contraseña incorrectos")
    except Exception as e:
        return render_template('login.html', error=f"Error: {str(e)}")

@app.route('/api/search')
def api_search():
    """API endpoint para búsqueda - VULNERABLE"""
    username = request.args.get('username', '')
    
    if not username:
        return jsonify({'error': 'Username parameter required'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # ¡VULNERABLE!
        query = f"SELECT id, username, email FROM users WHERE username LIKE '%{username}%'"
        
        print(f"[VULNERABLE] Ejecutando query: {query}")
        cursor.execute(query)
        
        users_list = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify({'users': users_list, 'count': len(users_list)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
