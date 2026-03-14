# Guía de Inicio Rápido

Esta guía te ayudará a poner en marcha ambas versiones de la aplicación en menos de 5 minutos.

## Prerequisitos

Asegúrate de tener instalado:

- ✅ [Docker Desktop](https://www.docker.com/products/docker-desktop) (Windows/Mac) o Docker Engine (Linux)
- ✅ [Docker Compose](https://docs.docker.com/compose/install/) (incluido en Docker Desktop)
- ✅ [Git](https://git-scm.com/downloads) (para clonar el repositorio)

### Verificar Instalación

```bash
docker --version
docker-compose --version
git --version
```

## Paso 1: Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd SQLInjectionDemo
```

## Paso 2: Iniciar Versión Vulnerable (v1.0)

```bash
cd v1.0-vulnerable
docker-compose up -d
```

**Espera unos segundos** mientras Docker descarga las imágenes y construye los contenedores.

### Verificar que está corriendo:

```bash
docker-compose ps
```

Deberías ver:

```
NAME                   STATUS
sqli_vulnerable_db     Up
sqli_vulnerable_web    Up
```

### Acceder a la aplicación:

Abre tu navegador en: **http://localhost:5000**

## Paso 3: Probar la Vulnerabilidad

### Opción A: Prueba Manual

1. Ve a: http://localhost:5000/search
2. Ingresa: `' OR '1'='1`
3. Observa que muestra **todos los usuarios con contraseñas**

### Opción B: Prueba con sqlmap

```bash
# Instalar sqlmap (si no lo tienes)
pip install sqlmap

# Ejecutar ataque básico
sqlmap -u "http://localhost:5000/search?username=test" --dbs --batch
```

## Paso 4: Iniciar Versión Segura (v2.0)

En una **nueva terminal**:

```bash
cd v2.0-secure
docker-compose up -d
```

### Acceder a la aplicación segura:

Abre tu navegador en: **http://localhost:5001**

## Paso 5: Verificar la Protección

### Opción A: Prueba Manual

1. Ve a: http://localhost:5001/search
2. Ingresa: `' OR '1'='1`
3. Observa que **NO muestra resultados** (payload sanitizado)

### Opción B: Prueba con sqlmap

```bash
sqlmap -u "http://localhost:5001/search?username=test" --dbs --batch
```

Deberías ver: `parameter 'username' does not seem to be injectable`

## Comparación Lado a Lado

| Aspecto | v1.0 (Puerto 5000) | v2.0 (Puerto 5001) |
|---------|-------------------|-------------------|
| **URL** | http://localhost:5000 | http://localhost:5001 |
| **Payload: `' OR '1'='1`** | ✅ Funciona (muestra todo) | ❌ Bloqueado |
| **sqlmap** | ✅ Puede explotar | ❌ No puede explotar |
| **Seguridad** | ❌ Vulnerable | ✅ Protegida |

## Detener las Aplicaciones

### Detener v1.0:

```bash
cd v1.0-vulnerable
docker-compose down
```

### Detener v2.0:

```bash
cd v2.0-secure
docker-compose down
```

### Detener ambas y limpiar:

```bash
# Desde la raíz del proyecto
cd v1.0-vulnerable && docker-compose down && cd ..
cd v2.0-secure && docker-compose down && cd ..
```

## Ver Logs

### v1.0:

```bash
cd v1.0-vulnerable
docker-compose logs -f web
```

### v2.0:

```bash
cd v2.0-secure
docker-compose logs -f web
```

Presiona `Ctrl+C` para salir de los logs.

## Solución de Problemas

### Error: "Port already in use"

Si el puerto 5000 o 5001 ya está en uso:

**Windows:**
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -ti:5000 | xargs kill -9
```

### Error: "Cannot connect to Docker daemon"

Asegúrate de que Docker Desktop esté corriendo:

- **Windows/Mac**: Abre Docker Desktop
- **Linux**: `sudo systemctl start docker`

### Error: "Database connection failed"

Espera unos segundos más. La base de datos tarda en inicializarse.

Verifica el estado:

```bash
docker-compose ps
docker-compose logs db
```

### Reiniciar desde cero:

```bash
# v1.0
cd v1.0-vulnerable
docker-compose down -v  # -v elimina los volúmenes
docker-compose up -d

# v2.0
cd v2.0-secure
docker-compose down -v
docker-compose up -d
```

## Próximos Pasos

1. 📖 Lee [COMPARISON.md](COMPARISON.md) para entender las diferencias de código
2. 🔍 Revisa [SQLMAP_GUIDE.md](SQLMAP_GUIDE.md) para ataques avanzados
3. 💻 Examina el código fuente en `app/app.py` de ambas versiones
4. 🧪 Experimenta con diferentes payloads de SQL Injection

## Datos de Prueba

### Usuarios disponibles:

| Username | Password |
|----------|----------|
| admin | admin123 |
| john_doe | password123 |
| jane_smith | mypassword |
| bob_wilson | secret456 |
| alice_brown | pass789 |

### Endpoints disponibles:

- `/` - Página principal
- `/users` - Lista de usuarios
- `/search` - Búsqueda (vulnerable en v1.0)
- `/login` - Login (vulnerable en v1.0)
- `/api/search` - API endpoint
- `/health` - Health check

## Recursos Adicionales

- 📚 [README.md](README.md) - Documentación completa
- 🔐 [COMPARISON.md](COMPARISON.md) - Comparación detallada
- ⚔️ [SQLMAP_GUIDE.md](SQLMAP_GUIDE.md) - Guía de sqlmap
- 📜 [LICENSE](LICENSE) - Licencia y advertencias

## Advertencia

⚠️ **SOLO PARA FINES EDUCATIVOS**

Esta aplicación vulnerable está diseñada únicamente con fines educativos. **NO** la uses en entornos de producción ni para actividades maliciosas. El uso de técnicas de SQL Injection en sistemas sin autorización es ilegal.

## Soporte

Si encuentras problemas:

1. Revisa la sección de Solución de Problemas arriba
2. Verifica los logs: `docker-compose logs`
3. Asegúrate de que Docker esté corriendo
4. Verifica que los puertos 5000 y 5001 estén libres

---

**¡Feliz aprendizaje! 🎓🔒**
