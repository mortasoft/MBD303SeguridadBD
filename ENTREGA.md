# Documento de Entrega - Proyecto SQL Injection

## Información del Proyecto

**Título**: Demostración de SQL Injection - Versión Vulnerable y Segura  
**Tecnologías**: Python (Flask), MySQL, Docker, Docker Compose  
**Fecha de Creación**: Marzo 2024  

## Descripción

Este proyecto contiene dos versiones de una aplicación web de gestión de usuarios:

1. **v1.0-vulnerable**: Aplicación intencionalmente vulnerable a ataques de SQL Injection
2. **v2.0-secure**: Aplicación protegida mediante sanitización de entrada y consultas parametrizadas

## Contenido del Repositorio

### Archivos Principales

- **README.md**: Documentación principal del proyecto
- **QUICK_START.md**: Guía de inicio rápido (5 minutos)
- **COMPARISON.md**: Comparación detallada entre versión vulnerable y segura
- **SQLMAP_GUIDE.md**: Guía completa para usar sqlmap
- **GITHUB_SETUP.md**: Instrucciones para subir a GitHub
- **LICENSE**: Licencia MIT y advertencias de uso educativo
- **.gitignore**: Archivos excluidos del repositorio

### Versión 1.0 - Vulnerable

**Ubicación**: `v1.0-vulnerable/`

**Estructura**:
```
v1.0-vulnerable/
├── docker-compose.yml          # Configuración de contenedores
├── app/
│   ├── Dockerfile             # Imagen de la aplicación web
│   ├── app.py                 # Aplicación Flask VULNERABLE
│   ├── requirements.txt       # Dependencias Python
│   └── templates/             # Templates HTML
│       ├── index.html         # Página principal
│       ├── users.html         # Lista de usuarios
│       ├── search.html        # Búsqueda vulnerable
│       └── login.html         # Login vulnerable
└── db/
    └── init.sql               # Script de inicialización de BD
```

**Características**:
- ❌ Concatenación directa de SQL
- ❌ Sin sanitización de entrada
- ❌ Sin validación de parámetros
- ❌ Expone contraseñas en resultados
- ❌ Mensajes de error detallados

**Puerto**: 5000  
**URL**: http://localhost:5000

### Versión 2.0 - Segura

**Ubicación**: `v2.0-secure/`

**Estructura**:
```
v2.0-secure/
├── docker-compose.yml          # Configuración de contenedores
├── app/
│   ├── Dockerfile             # Imagen de la aplicación web
│   ├── app.py                 # Aplicación Flask SEGURA
│   ├── requirements.txt       # Dependencias Python
│   └── templates/             # Templates HTML
│       ├── index.html         # Página principal
│       ├── users.html         # Lista de usuarios
│       ├── search.html        # Búsqueda segura
│       └── login.html         # Login seguro
└── db/
    └── init.sql               # Script de inicialización de BD
```

**Características**:
- ✅ Consultas parametrizadas (Prepared Statements)
- ✅ Sanitización de entrada con regex
- ✅ Validación de formato de datos
- ✅ No expone contraseñas
- ✅ Mensajes de error genéricos

**Puerto**: 5001  
**URL**: http://localhost:5001

## Tecnologías Utilizadas

### Backend
- **Python 3.11**: Lenguaje de programación
- **Flask 3.0**: Framework web
- **mysql-connector-python 8.2**: Conector de base de datos

### Base de Datos
- **MySQL 8.0**: Sistema de gestión de base de datos

### Containerización
- **Docker**: Plataforma de contenedores
- **Docker Compose**: Orquestación de contenedores

### Herramientas de Testing
- **sqlmap**: Herramienta de explotación de SQL Injection

## Instrucciones de Ejecución

### Requisitos Previos
- Docker Desktop instalado
- Docker Compose instalado
- Puertos 5000 y 5001 disponibles

### Ejecutar Versión Vulnerable

```bash
cd v1.0-vulnerable
docker-compose up -d
```

Acceder en: http://localhost:5000

### Ejecutar Versión Segura

```bash
cd v2.0-secure
docker-compose up -d
```

Acceder en: http://localhost:5001

### Detener Aplicaciones

```bash
docker-compose down
```

## Demostración de Vulnerabilidad

### Prueba Manual

1. Ir a: http://localhost:5000/search
2. Ingresar payload: `' OR '1'='1`
3. Resultado: Muestra todos los usuarios con contraseñas

### Prueba con sqlmap

```bash
# Enumerar bases de datos
sqlmap -u "http://localhost:5000/search?username=test" --dbs --batch

# Dump completo de la base de datos
sqlmap -u "http://localhost:5000/search?username=test" -D userdb --dump-all --batch
```

## Demostración de Protección

### Prueba Manual

1. Ir a: http://localhost:5001/search
2. Ingresar payload: `' OR '1'='1`
3. Resultado: No encuentra resultados (payload sanitizado)

### Prueba con sqlmap

```bash
sqlmap -u "http://localhost:5001/search?username=test" --dbs --batch
```

Resultado esperado: `parameter 'username' does not seem to be injectable`

## Diferencias Clave en el Código

### Vulnerable (v1.0)

```python
# ❌ VULNERABLE - Concatenación directa
username = request.args.get('username', '')
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)
```

### Segura (v2.0)

```python
# ✅ SEGURA - Consulta parametrizada
username = request.args.get('username', '')
username_sanitized = sanitize_input(username)
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (username_sanitized,))
```

## Medidas de Seguridad Implementadas

### 1. Consultas Parametrizadas
Uso de placeholders (`%s`) en lugar de concatenación de strings.

### 2. Sanitización de Entrada
```python
def sanitize_input(input_string):
    sanitized = re.sub(r'[^\w\s\-@.]', '', input_string)
    sanitized = sanitized[:100]
    return sanitized
```

### 3. Validación de Formato
```python
def validate_username(username):
    pattern = r'^[a-zA-Z0-9_]{3,50}$'
    return bool(re.match(pattern, username))
```

### 4. Principio de Mínimo Privilegio
- No exponer contraseñas en resultados de búsqueda
- Mensajes de error genéricos
- No revelar estructura de base de datos

## Datos de Prueba

### Usuarios Disponibles

| Username | Password | Email |
|----------|----------|-------|
| admin | admin123 | admin@example.com |
| john_doe | password123 | john@example.com |
| jane_smith | mypassword | jane@example.com |
| bob_wilson | secret456 | bob@example.com |
| alice_brown | pass789 | alice@example.com |

### Tablas en la Base de Datos

1. **users**: Información de usuarios (id, username, email, password)
2. **sensitive_data**: Datos sensibles (credit_card, ssn, secret_key)

## Payloads de SQL Injection Probados

### Payloads que Funcionan en v1.0

- `' OR '1'='1` - Bypass de autenticación
- `' OR 1=1--` - Bypass con comentario
- `admin'--` - Bypass con comentario
- `' UNION SELECT NULL,NULL,NULL,NULL--` - Union-based injection
- `' UNION SELECT 1,username,password,email FROM users--` - Extracción de datos

### Payloads Bloqueados en v2.0

Todos los payloads anteriores son sanitizados y no funcionan en la versión segura.

## Resultados de Pruebas con sqlmap

### v1.0 - Vulnerable ✅ Explotable

```
[INFO] the back-end DBMS is MySQL
[INFO] fetching database names
available databases [4]:
[*] userdb
```

### v2.0 - Segura ❌ No Explotable

```
[WARNING] parameter 'username' does not seem to be injectable
[CRITICAL] all tested parameters do not appear to be injectable
```

## Documentación Incluida

1. **README.md**: Documentación completa del proyecto
2. **QUICK_START.md**: Guía de inicio rápido
3. **COMPARISON.md**: Comparación detallada de código
4. **SQLMAP_GUIDE.md**: Tutorial completo de sqlmap
5. **GITHUB_SETUP.md**: Instrucciones para GitHub
6. **ENTREGA.md**: Este documento

## Conclusiones

Este proyecto demuestra:

1. **Vulnerabilidad**: Cómo las consultas SQL mal construidas permiten ataques de inyección
2. **Explotación**: Uso de sqlmap para extraer información de bases de datos vulnerables
3. **Mitigación**: Implementación de consultas parametrizadas y sanitización de entrada
4. **Verificación**: Comprobación de que las medidas de seguridad previenen los ataques

## Lecciones Aprendidas

1. ✅ **NUNCA** concatenar directamente entrada del usuario en consultas SQL
2. ✅ **SIEMPRE** usar consultas parametrizadas (prepared statements)
3. ✅ **VALIDAR** toda entrada del usuario
4. ✅ **SANITIZAR** caracteres especiales
5. ✅ **NO EXPONER** información sensible en mensajes de error
6. ✅ **APLICAR** el principio de mínimo privilegio

## Advertencias

⚠️ **SOLO PARA FINES EDUCATIVOS**

- Esta aplicación vulnerable está diseñada únicamente con fines educativos
- **NO** debe ser utilizada en entornos de producción
- El uso de técnicas de SQL Injection en sistemas sin autorización es **ILEGAL**
- Siempre obtén autorización explícita antes de realizar pruebas de seguridad

## Referencias

- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)
- [sqlmap Documentation](https://github.com/sqlmapproject/sqlmap/wiki)
- [MySQL Prepared Statements](https://dev.mysql.com/doc/refman/8.0/en/sql-prepared-statements.html)

## Licencia

MIT License - Ver archivo [LICENSE](LICENSE) para más detalles.

---

## Checklist de Entrega

- ✅ Versión 1.0 vulnerable desarrollada
- ✅ Versión 2.0 segura desarrollada
- ✅ Docker Compose para ambas versiones
- ✅ Documentación completa
- ✅ Guía de uso de sqlmap
- ✅ Instrucciones para GitHub
- ✅ .gitignore configurado
- ✅ LICENSE incluido
- ✅ README.md completo

## Enlace del Repositorio

**Pendiente**: Subir a GitHub siguiendo las instrucciones en [GITHUB_SETUP.md](GITHUB_SETUP.md)

Una vez subido, el enlace será:
```
https://github.com/TU_USUARIO/SQLInjectionDemo
```

---

**Proyecto completado exitosamente. Listo para entrega. ✅**
