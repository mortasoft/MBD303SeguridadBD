# Ejecución Manual Sin Docker

Si no puedes usar Docker, sigue estos pasos para ejecutar la aplicación directamente.

## Prerequisitos

1. **Python 3.11+** instalado
2. **MySQL 8.0** instalado y corriendo
3. **pip** (gestor de paquetes de Python)

## Paso 1: Verificar Instalaciones

```powershell
python --version
mysql --version
pip --version
```

## Paso 2: Configurar Base de Datos

### Opción A: Desde línea de comandos MySQL

```powershell
# Conectar a MySQL
mysql -u root -p

# En el prompt de MySQL, ejecutar:
```

```sql
CREATE DATABASE IF NOT EXISTS userdb;
USE userdb;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, email, password) VALUES
('admin', 'admin@example.com', 'admin123'),
('john_doe', 'john@example.com', 'password123'),
('jane_smith', 'jane@example.com', 'mypassword'),
('bob_wilson', 'bob@example.com', 'secret456'),
('alice_brown', 'alice@example.com', 'pass789'),
('charlie_davis', 'charlie@example.com', 'qwerty123'),
('diana_miller', 'diana@example.com', 'letmein'),
('edward_jones', 'edward@example.com', 'password1'),
('fiona_garcia', 'fiona@example.com', 'welcome123'),
('george_martinez', 'george@example.com', 'abc123');

CREATE TABLE IF NOT EXISTS sensitive_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    credit_card VARCHAR(16),
    ssn VARCHAR(11),
    secret_key VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO sensitive_data (user_id, credit_card, ssn, secret_key) VALUES
(1, '4532123456789012', '123-45-6789', 'ADMIN_SECRET_KEY_2024'),
(2, '5425123456789012', '234-56-7890', 'USER_SECRET_KEY_ABC'),
(3, '4916123456789012', '345-67-8901', 'PRIVATE_KEY_XYZ123'),
(4, '6011123456789012', '456-78-9012', 'CONFIDENTIAL_DATA_456'),
(5, '3782123456789012', '567-89-0123', 'SECRET_TOKEN_789');

exit;
```

### Opción B: Importar desde archivo SQL

```powershell
# Navegar a la carpeta del proyecto
cd c:\Users\trian\OneDrive\WWT\SQLInjectionDemo\v1.0-vulnerable\db

# Importar el archivo SQL
mysql -u root -p < init.sql
```

## Paso 3: Ejecutar Versión Vulnerable (v1.0)

```powershell
# Navegar a la carpeta de la aplicación
cd c:\Users\trian\OneDrive\WWT\SQLInjectionDemo\v1.0-vulnerable\app

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (opcional, usa valores por defecto)
$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASSWORD="rootpassword"
$env:DB_NAME="userdb"

# Ejecutar la aplicación
python app.py
```

La aplicación estará disponible en: **http://localhost:5000**

## Paso 4: Ejecutar Versión Segura (v2.0)

En una **nueva terminal PowerShell**:

```powershell
# Navegar a la carpeta de la aplicación segura
cd c:\Users\trian\OneDrive\WWT\SQLInjectionDemo\v2.0-secure\app

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASSWORD="rootpassword"
$env:DB_NAME="userdb"

# Ejecutar la aplicación en puerto diferente
# Editar app.py y cambiar el puerto a 5001 en la última línea:
# app.run(host='0.0.0.0', port=5001, debug=True)

python app.py
```

La aplicación estará disponible en: **http://localhost:5001**

## Detener las Aplicaciones

Presiona `Ctrl+C` en cada terminal donde esté corriendo la aplicación.

## Solución de Problemas

### Error: "Access denied for user 'root'"

Verifica la contraseña de MySQL:

```powershell
mysql -u root -p
# Ingresa tu contraseña de MySQL
```

Si la contraseña es diferente a `rootpassword`, actualiza las variables de entorno:

```powershell
$env:DB_PASSWORD="tu_password_real"
```

### Error: "Can't connect to MySQL server"

Verifica que MySQL esté corriendo:

```powershell
# Verificar servicios de Windows
Get-Service -Name MySQL*
```

Si no está corriendo, inícialo:

```powershell
Start-Service -Name MySQL80
```

### Error: "ModuleNotFoundError: No module named 'flask'"

Instala las dependencias:

```powershell
pip install Flask mysql-connector-python
```

### Puerto 5000 ya en uso

Cambia el puerto en `app.py`:

```python
# Última línea de app.py
app.run(host='0.0.0.0', port=5002, debug=True)  # Cambiar a 5002 o cualquier otro
```

## Probar la Aplicación

### Prueba Manual

1. Abre el navegador en: http://localhost:5000
2. Ve a "Buscar Usuario"
3. Ingresa: `' OR '1'='1`
4. Observa que muestra todos los usuarios

### Probar con sqlmap

```powershell
# Instalar sqlmap
pip install sqlmap

# Ejecutar ataque
sqlmap -u "http://localhost:5000/search?username=test" --dbs --batch
```

## Usuarios de Prueba

| Username | Password |
|----------|----------|
| admin | admin123 |
| john_doe | password123 |
| jane_smith | mypassword |

## Notas Importantes

1. **Seguridad**: Asegúrate de que MySQL solo acepte conexiones locales
2. **Firewall**: Puede que necesites permitir Python en el firewall de Windows
3. **Antivirus**: Algunos antivirus pueden bloquear conexiones locales
4. **Base de datos**: Ambas versiones usan la misma base de datos `userdb`

## Volver a Docker (Recomendado)

Una vez que instales Docker Desktop, podrás ejecutar todo con un solo comando:

```powershell
docker-compose up -d
```

Esto es mucho más simple y no requiere configurar MySQL manualmente.
