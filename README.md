# 🚀 FastAPI RouteMaster - Sistema de Gestión Comercial

Una API moderna y escalable construida con FastAPI, SQL Server y autenticación JWT. Diseñada para sistemas de gestión comercial con roles, permisos y flujo completo de ventas.

## ✨ Características

### 🔐 Autenticación & Seguridad
- **JWT Tokens** - Autenticación stateless con tokens seguros
- **Validación de contraseñas** - Mínimo 8 caracteres con reglas de complejidad
- **Roles y permisos** - Sistema flexible de roles basado en base de datos
- **Rate Limiting** - Protección contra ataques de fuerza bruta
- **Variables de entorno** - Configuración segura y separada

### 🗄️ Base de Datos
- **SQL Server** - Base de datos empresarial
- **SQLAlchemy ORM** - Abstracción de base de datos
- **Modelos relacionales** - Estructura escalable y normalizada
- **Migraciones automáticas** - Control de versiones de esquema

### 🛠️ Arquitectura
- **Arquitectura modular** - Separación de concerns (routes, models, schemas, crud)
- **Documentación automática** - Swagger UI y ReDoc integrados
- **Type hints** - Código más maintainable y menos propenso a errores
- **Validación de datos** - Con Pydantic v2

### 📦 Módulos Implementados
- **🔐 Autenticación** - Login, registro, gestión de tokens
- **👥 Gestión de Usuarios** - CRUD completo con roles y permisos
- **🏢 Gestión de Clientes** - CRM básico con NIT único
- **📦 Gestión de Productos** - Inventario con control de stock
- **🛒 Gestión de Pedidos** - Sistema completo de ventas con cálculos automáticos
- **📋 Detalles de Pedidos** - Items de pedido con subtotales
- **🚚 Módulo de Entregas** - Seguimiento de estado de entregas
- **💰 Módulo de Cobros** - Gestión de pagos y facturación
- **🗺️ Gestión de Rutas** - Asignación y planificación de rutas

## 📊 Roles del Sistema

| Rol | Descripción | Permisos |
|-----|-------------|----------|
| **Gerente** | Administra usuarios y consulta reportes | Gestión de usuarios, reportes, configuración del sistema |
| **Administrador** | Gestiona productos y rutas | Gestión de productos, rutas, clientes |
| **Vendedor** | Registra clientes y pedidos | CRUD clientes, pedidos, consulta productos |
| **Repartidor** | Confirma entregas y registra cobros | Gestión de entregas, cobros, actualización de estados |
| **Usuario Sistema** | Acceso básico al sistema | Autenticación básica, perfil propio |

## 🚀 Instalación Rápida

### Prerrequisitos
- Python 3.10+
- SQL Server 2019+
- Docker (opcional, para SQL Server)

### 1. Clonar y configurar
```bash
git clone <tu-repo-url>
cd api_routeMaster
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

pip install -r requirements.txt
```
### 2. Clonar y configurar
```bash
cp .env.example .env
# Editar .env con tus configuraciones de base de datos
```
### 3. Clonar y configurar
```bash
# Las tablas se crean automáticamente al iniciar la aplicación
python app/scripts/setup_database.py
```


### 4. Ejecutar la aplicacion
```bash
uvicorn app.main:app --reload
```



### 📚 Documentación de API
Una vez ejecutada la aplicación, accede a:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

### 🔄 Flujo Comercial Implementado
1. 📝 Crear Cliente → Registrar información del cliente

2. 📦 Gestionar Productos → Mantener inventario actualizado

3. 🛒 Crear Pedido → Registrar venta con múltiples productos

4. 📋 Detalles Automáticos → Cálculo de subtotales y total

5. 📦 Gestión de Stock → Actualización automática de inventario

6. 🚚 Seguimiento de Entrega → Estados: Pendiente, Entregado, Rechazado

7. 💰 Registro de Cobro → Gestión de pagos y facturación

### 🛣️ Endpoints Principales
- Autenticación
  - POST /auth/login — Iniciar sesión
  - POST /auth/register — Registrar nuevo usuario

- Gestión de Clientes
  - GET /clientes — Listar clientes
  - POST /clientes — Crear cliente

- Gestión de Productos
  - GET /productos — Listar productos
  - POST /productos — Crear/actualizar productos

- Pedidos (Ventas)
  - GET /pedidos — Listar pedidos
  - POST /pedidos — Crear nuevo pedido

- Entregas
  - GET /entregas — Listar entregas
  - POST /entregas — Registrar/actualizar entrega

- Cobros / Facturación
  - GET /cobros — Listar cobros
  - POST /cobros — Registrar cobro

### 🎯 Estado del Proyecto
- ✅ Completado
  - Sistema de autenticación JWT
  - Gestión de usuarios, roles y permisos
  - CRUD completo de clientes
  - CRUD completo de productos con control de stock
  - Sistema de pedidos con cálculos automáticos
  - Módulo de entregas con seguimiento de estados
  - Módulo de cobros con gestión de pagos
  - Validación de datos con Pydantic
  - Documentación automática con Swagger

- 🔄 En desarrollo
  - Dashboard con reportes y estadísticas
  - Sistema de notificaciones
  - Integración con APIs de pagos
  - Módulo de facturación electrónica

📄 Licencia
Distribuido bajo la Licencia MIT. Ver LICENSE para más información.

🆘 Soporte
Si encuentras algún problema o tienes preguntas:

- Revisa la documentación en /docs

- Abre un issue en el repositorio

- Contacta al equipo de desarrollo