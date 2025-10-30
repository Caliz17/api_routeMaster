# 🚀 FastAPI Auth & Management API

Una API moderna y escalable construida con FastAPI, SQL Server y autenticación JWT. Diseñada para sistemas de gestión con roles y permisos.

## ✨ Características

### 🔐 Autenticación & Seguridad
- **JWT Tokens** - Autenticación stateless con tokens seguros
- **Validación de contraseñas** - Mínimo 8 caracteres con reglas de complejidad
- **Roles y permisos** - Sistema flexible de roles basado en base de datos
- **Rate Limiting** - Protección contra ataques de fuerza bruta
- **Variables de entorno** - Configuración segura y separada

### 🗄️ Base de Datos
- **SQL Server** - Base de datos empresarial
- **SQLAlchemy ORM** - Abstraction de base de datos
- **Modelos relacionales** - Estructura escalable y normalizada
- **Migraciones** - Control de versiones de esquema

### 🛠️ Desarrollo
- **Arquitectura modular** - Separación de concerns (routes, models, schemas, crud)
- **Documentación automática** - Swagger UI y ReDoc integrados
- **Type hints** - Código más maintainable y menos propenso a errores
- **Validación de datos** - Con Pydantic v2

### 📊 Roles del Sistema
| Rol | Descripción | Permisos |
|-----|-------------|----------|
| **Gerente** | Administra usuarios y consulta reportes | Gestión de usuarios, reportes |
| **Administrador** | Gestiona rutas y productos | Gestión de productos, rutas |
| **Vendedor** | Registra clientes y pedidos | CRUD clientes, pedidos |
| **Repartidor** | Confirma entregas y registra cobros | Gestión de entregas, cobros |
| **Usuario Sistema** | Acceso básico al sistema | Autenticación básica |

## 🚀 Instalación Rápida

### Prerrequisitos
- Python 3.10+
- SQL Server 2022+
- Docker (opcional, para SQL Server)

### 1. Clonar y configurar
```bash
git clone <tu-repo-url>
cd fastapi_auth
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows