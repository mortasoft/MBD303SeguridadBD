# Guía para Subir el Proyecto a GitHub

Esta guía te ayudará a crear un repositorio en GitHub y subir el código fuente de ambas aplicaciones.

## Opción 1: Usar tu Cuenta Personal de GitHub

### Paso 1: Crear una Cuenta en GitHub (si no tienes)

1. Ve a [github.com](https://github.com)
2. Haz clic en "Sign up"
3. Completa el registro con tu email personal

### Paso 2: Crear un Nuevo Repositorio

1. Inicia sesión en GitHub
2. Haz clic en el botón **"+"** en la esquina superior derecha
3. Selecciona **"New repository"**
4. Completa los datos:
   - **Repository name**: `SQLInjectionDemo` o `sql-injection-demo`
   - **Description**: `Demostración educativa de SQL Injection - Versión vulnerable y segura`
   - **Visibility**: Selecciona **Public** (público)
   - ✅ Marca **"Add a README file"** (NO - ya tenemos uno)
   - ✅ Marca **"Add .gitignore"** (NO - ya tenemos uno)
   - Selecciona **"Choose a license"**: MIT License (NO - ya tenemos uno)
5. Haz clic en **"Create repository"**

### Paso 3: Subir el Código

Abre una terminal en la carpeta del proyecto:

```bash
cd c:\Users\trian\OneDrive\WWT\SQLInjectionDemo
```

Inicializa Git y sube el código:

```bash
# Inicializar repositorio Git
git init

# Agregar todos los archivos
git add .

# Hacer el primer commit
git commit -m "Initial commit: SQL Injection Demo - Vulnerable and Secure versions"

# Agregar el repositorio remoto (reemplaza TU_USUARIO con tu nombre de usuario)
git remote add origin https://github.com/TU_USUARIO/SQLInjectionDemo.git

# Cambiar a la rama main
git branch -M main

# Subir el código
git push -u origin main
```

**Nota**: Reemplaza `TU_USUARIO` con tu nombre de usuario de GitHub.

### Paso 4: Verificar

1. Ve a tu repositorio en GitHub: `https://github.com/TU_USUARIO/SQLInjectionDemo`
2. Verifica que todos los archivos estén presentes
3. El README.md debería mostrarse automáticamente

## Opción 2: Usar Correo de la Universidad

### Paso 1: Crear Cuenta con Email Universitario

1. Ve a [github.com](https://github.com)
2. Haz clic en "Sign up"
3. Usa tu correo universitario (ej: `tunombre@universidad.edu`)
4. Completa el registro

### Paso 2: Solicitar GitHub Student Developer Pack (Opcional)

1. Ve a [education.github.com/pack](https://education.github.com/pack)
2. Haz clic en "Get your pack"
3. Verifica tu email universitario
4. Obtén beneficios gratuitos (repositorios privados ilimitados, GitHub Copilot, etc.)

### Paso 3: Crear Repositorio y Subir Código

Sigue los mismos pasos que en la Opción 1, Pasos 2-4.

## Estructura del Repositorio

Tu repositorio debería tener esta estructura:

```
SQLInjectionDemo/
├── .gitignore
├── README.md
├── LICENSE
├── QUICK_START.md
├── COMPARISON.md
├── SQLMAP_GUIDE.md
├── GITHUB_SETUP.md
├── v1.0-vulnerable/
│   ├── docker-compose.yml
│   ├── app/
│   │   ├── Dockerfile
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── templates/
│   │       ├── index.html
│   │       ├── users.html
│   │       ├── search.html
│   │       └── login.html
│   └── db/
│       └── init.sql
└── v2.0-secure/
    ├── docker-compose.yml
    ├── app/
    │   ├── Dockerfile
    │   ├── app.py
    │   ├── requirements.txt
    │   └── templates/
    │       ├── index.html
    │       ├── users.html
    │       ├── search.html
    │       └── login.html
    └── db/
        └── init.sql
```

## Comandos Git Útiles

### Ver el estado de los archivos

```bash
git status
```

### Agregar archivos específicos

```bash
git add archivo.txt
git add carpeta/
```

### Hacer commit de cambios

```bash
git commit -m "Descripción del cambio"
```

### Subir cambios

```bash
git push
```

### Ver el historial

```bash
git log
```

### Clonar tu repositorio en otra computadora

```bash
git clone https://github.com/TU_USUARIO/SQLInjectionDemo.git
```

## Personalizar el README

Antes de subir, puedes personalizar el README.md:

1. Abre `README.md` en un editor de texto
2. Agrega tu nombre o información del curso
3. Actualiza la sección de autor

Ejemplo:

```markdown
## Autor

**Nombre**: Tu Nombre
**Universidad**: Universidad XYZ
**Curso**: Seguridad en Aplicaciones Web
**Fecha**: Marzo 2024
```

## Agregar Badges al README (Opcional)

Puedes agregar badges al inicio del README para que se vea más profesional:

```markdown
# SQL Injection Demo

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)
```

## Compartir el Enlace

Una vez subido, comparte el enlace del repositorio:

```
https://github.com/TU_USUARIO/SQLInjectionDemo
```

Este es el enlace que debes entregar como parte de tu asignación.

## Hacer el Repositorio Privado (Opcional)

Si prefieres que el repositorio sea privado:

1. Ve a tu repositorio en GitHub
2. Haz clic en **"Settings"**
3. Desplázate hasta **"Danger Zone"**
4. Haz clic en **"Change visibility"**
5. Selecciona **"Make private"**
6. Confirma la acción

**Nota**: Si haces el repositorio privado, deberás dar acceso al profesor:

1. Ve a **"Settings"** → **"Collaborators"**
2. Haz clic en **"Add people"**
3. Ingresa el usuario de GitHub del profesor
4. Envía la invitación

## Actualizar el Repositorio

Si haces cambios después de subir el código:

```bash
# Ver qué archivos cambiaron
git status

# Agregar los cambios
git add .

# Hacer commit
git commit -m "Descripción de los cambios"

# Subir los cambios
git push
```

## Solución de Problemas

### Error: "remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/SQLInjectionDemo.git
```

### Error: "failed to push some refs"

```bash
git pull origin main --rebase
git push -u origin main
```

### Error: "Permission denied"

Configura tus credenciales:

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

### Autenticación con Token Personal

GitHub ya no permite autenticación con contraseña. Necesitas un token:

1. Ve a GitHub → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Haz clic en **"Generate new token"**
3. Selecciona los permisos necesarios (repo)
4. Copia el token
5. Úsalo como contraseña cuando Git te lo pida

## Verificación Final

Antes de entregar, verifica:

- ✅ El repositorio es público (o el profesor tiene acceso si es privado)
- ✅ Todos los archivos están presentes
- ✅ El README.md se muestra correctamente
- ✅ Los archivos Docker están incluidos
- ✅ La documentación está completa
- ✅ El .gitignore está funcionando (no hay archivos innecesarios)

## Ejemplo de Enlace Final

Tu enlace debería verse así:

```
https://github.com/juan-perez/SQLInjectionDemo
```

O si usas el correo universitario:

```
https://github.com/jperez-universidad/SQLInjectionDemo
```

## Recursos Adicionales

- [GitHub Docs](https://docs.github.com)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [GitHub Student Developer Pack](https://education.github.com/pack)
- [Markdown Guide](https://www.markdownguide.org/)

---

**¡Listo! Tu proyecto está en GitHub y listo para entregar. 🎉**
