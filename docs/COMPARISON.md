# Comparación: Versión Vulnerable vs Versión Segura

Este documento compara las diferencias clave entre la versión vulnerable (v1.0) y la versión segura (v2.0) de la aplicación.

## Tabla Comparativa

| Aspecto | v1.0 Vulnerable | v2.0 Segura |
|---------|----------------|-------------|
| **Puerto** | 5000 | 5001 |
| **Consultas SQL** | Concatenación directa | Consultas parametrizadas |
| **Sanitización** | ❌ No | ✅ Sí |
| **Validación** | ❌ No | ✅ Sí |
| **Mensajes de error** | Detallados (exponen información) | Genéricos |
| **Protección SQL Injection** | ❌ No | ✅ Sí |

## Diferencias en el Código

### Búsqueda de Usuarios

#### v1.0 - VULNERABLE ❌

```python
@app.route('/search')
def search():
    username = request.args.get('username', '')
    
    # ¡VULNERABLE! - Concatenación directa
    query = f"SELECT id, username, email, password FROM users WHERE username = '{username}'"
    
    cursor.execute(query)
    users_list = cursor.fetchall()
```

**Problemas:**
- Concatenación directa de strings
- Sin sanitización de entrada
- Sin validación
- Expone contraseñas en resultados

#### v2.0 - SEGURA ✅

```python
@app.route('/search')
def search():
    username = request.args.get('username', '')
    
    # Sanitizar entrada
    username_sanitized = sanitize_input(username)
    
    # ¡SEGURO! - Consulta parametrizada
    query = "SELECT id, username, email FROM users WHERE username = %s"
    
    cursor.execute(query, (username_sanitized,))
    users_list = cursor.fetchall()
```

**Mejoras:**
- Uso de placeholders (`%s`)
- Sanitización de entrada
- No expone contraseñas
- Parámetros pasados separadamente

### Login de Usuarios

#### v1.0 - VULNERABLE ❌

```python
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    # ¡VULNERABLE!
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    cursor.execute(query)
    user = cursor.fetchone()
```

**Ataques posibles:**
- `username: admin'--` → Bypass de autenticación
- `username: ' OR '1'='1` → Acceso sin credenciales

#### v2.0 - SEGURA ✅

```python
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    # Validar formato
    if not validate_username(username):
        return render_template('login.html', error="Formato inválido")
    
    # Sanitizar
    username_sanitized = sanitize_input(username)
    password_sanitized = sanitize_input(password)
    
    # ¡SEGURO!
    query = "SELECT id, username, email FROM users WHERE username = %s AND password = %s"
    
    cursor.execute(query, (username_sanitized, password_sanitized))
    user = cursor.fetchone()
```

**Protecciones:**
- Validación de formato
- Sanitización de entrada
- Consultas parametrizadas
- No expone información sensible

## Funciones de Seguridad en v2.0

### 1. Sanitización de Entrada

```python
def sanitize_input(input_string):
    """
    Sanitiza la entrada del usuario eliminando caracteres peligrosos
    """
    if not input_string:
        return ""
    
    # Eliminar caracteres potencialmente peligrosos
    sanitized = re.sub(r'[^\w\s\-@.]', '', input_string)
    
    # Limitar longitud
    sanitized = sanitized[:100]
    
    return sanitized
```

### 2. Validación de Username

```python
def validate_username(username):
    """
    Valida que el username tenga un formato correcto
    """
    if not username:
        return False
    
    # Solo permite letras, números y guiones bajos, entre 3 y 50 caracteres
    pattern = r'^[a-zA-Z0-9_]{3,50}$'
    return bool(re.match(pattern, username))
```

## Ejemplos de Payloads

### Payloads que Funcionan en v1.0 pero NO en v2.0

| Payload | Efecto en v1.0 | Efecto en v2.0 |
|---------|---------------|----------------|
| `' OR '1'='1` | ✅ Bypass autenticación | ❌ Sanitizado |
| `admin'--` | ✅ Bypass autenticación | ❌ Sanitizado |
| `' UNION SELECT NULL,NULL,NULL--` | ✅ Union injection | ❌ Bloqueado |
| `'; DROP TABLE users--` | ✅ Posible (si permisos) | ❌ Bloqueado |
| `' OR 1=1--` | ✅ Bypass | ❌ Sanitizado |

## Pruebas Manuales

### Probar v1.0 (Vulnerable)

1. Ir a: http://localhost:5000/search
2. Ingresar: `' OR '1'='1`
3. **Resultado**: Muestra todos los usuarios con contraseñas

### Probar v2.0 (Segura)

1. Ir a: http://localhost:5001/search
2. Ingresar: `' OR '1'='1`
3. **Resultado**: No encuentra resultados (payload sanitizado)

## Mejores Prácticas Implementadas en v2.0

### ✅ 1. Consultas Parametrizadas (Prepared Statements)

**Antes:**
```python
query = f"SELECT * FROM users WHERE id = {user_id}"
```

**Después:**
```python
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

### ✅ 2. Sanitización de Entrada

Eliminar o escapar caracteres especiales:
- Comillas simples (`'`)
- Comillas dobles (`"`)
- Punto y coma (`;`)
- Guiones (`--`)
- Barras (`/`, `\`)

### ✅ 3. Validación de Entrada

Verificar:
- Tipo de dato correcto
- Longitud apropiada
- Formato esperado (regex)
- Caracteres permitidos

### ✅ 4. Principio de Mínimo Privilegio

- No exponer contraseñas en resultados
- Mensajes de error genéricos
- No revelar estructura de BD

### ✅ 5. Manejo de Errores

**Antes:**
```python
except Exception as e:
    return f"Error: {str(e)}", 500  # Expone detalles
```

**Después:**
```python
except Exception as e:
    print(f"Error interno: {str(e)}")  # Log interno
    return "Error interno del servidor", 500  # Mensaje genérico
```

## Verificación con sqlmap

### v1.0 - Vulnerable

```bash
$ sqlmap -u "http://localhost:5000/search?username=test" --dbs --batch

[INFO] the back-end DBMS is MySQL
[INFO] fetching database names
available databases [4]:
[*] information_schema
[*] mysql
[*] performance_schema
[*] userdb
```

✅ **sqlmap puede explotar la vulnerabilidad**

### v2.0 - Segura

```bash
$ sqlmap -u "http://localhost:5001/search?username=test" --dbs --batch

[WARNING] parameter 'username' does not seem to be injectable
[CRITICAL] all tested parameters do not appear to be injectable
```

❌ **sqlmap NO puede explotar (protegida)**

## Impacto de las Vulnerabilidades

### v1.0 - Posibles Ataques

1. **Extracción de datos**: Robo de usuarios, contraseñas, datos sensibles
2. **Bypass de autenticación**: Acceso sin credenciales válidas
3. **Modificación de datos**: UPDATE, DELETE de registros
4. **Eliminación de tablas**: DROP TABLE (si permisos lo permiten)
5. **Ejecución de comandos**: En algunos casos, comandos del sistema

### v2.0 - Protecciones

1. ✅ Previene extracción de datos
2. ✅ Previene bypass de autenticación
3. ✅ Previene modificación no autorizada
4. ✅ Previene eliminación de tablas
5. ✅ Previene ejecución de comandos

## Conclusión

La diferencia fundamental entre ambas versiones es el uso de **consultas parametrizadas** combinado con **sanitización y validación de entrada**. Estas medidas simples pero efectivas previenen completamente los ataques de SQL Injection.

### Lecciones Clave

1. **NUNCA** concatenar directamente entrada del usuario en consultas SQL
2. **SIEMPRE** usar consultas parametrizadas (prepared statements)
3. **VALIDAR** toda entrada del usuario
4. **SANITIZAR** caracteres especiales
5. **NO EXPONER** información sensible en errores
6. **APLICAR** principio de mínimo privilegio

## Referencias

- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)
- [MySQL Prepared Statements](https://dev.mysql.com/doc/refman/8.0/en/sql-prepared-statements.html)
