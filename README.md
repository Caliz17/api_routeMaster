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
## 🧩 1. Instalar requisitos

### ✅ Requisitos mínimos:

- **Python 3.10+**
    
- **Git**
    
- **Docker Desktop**
    
- **SQL Server 2019+ (Docker o local)**
    

---

## 🧱 2. Instalar y preparar entorno

### 🧰 2.1 Instalar Git

Descarga desde:  
👉 [https://git-scm.com/downloads](https://git-scm.com/downloads)

Durante la instalación, deja las opciones por defecto.  
Cuando termines, abre **PowerShell** y verifica:

```bash
git --version
```

---

### 🐍 2.2 Instalar Python 3.12

Descarga desde:  
👉 [https://www.python.org/downloads/](https://www.python.org/downloads/)

Durante la instalación:

- ✅ Marca **“Add Python to PATH”**
    
- ✅ Instala para todos los usuarios
    

Verifica:

```bash
python --version
pip --version
```

---

## 🐳 3. Instalar y preparar Docker Desktop

Descarga desde:  
👉 [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

- Instálalo normalmente
    
- Reinicia Windows si lo pide
    
- Luego abre **Docker Desktop** y espera que diga:  
    ✅ _Docker Engine running_
    

Verifica desde PowerShell:

```bash
docker version
```

---

## 🧰 4. Levantar SQL Server en Docker

En PowerShell o CMD, ejecuta:

```bash
docker run -e "ACCEPT_EULA=Y" `
           -e "SA_PASSWORD=YourStrong!Passw0rd" `
           -p 1433:1433 `
           --name sqlserver `
           -d mcr.microsoft.com/mssql/server:2019-latest
```

> 💡 Puedes cambiar `YourStrong!Passw0rd` si quieres, pero debe tener:
> 
> - Mínimo 8 caracteres
>     
> - Una mayúscula
>     
> - Una minúscula
>     
> - Un número
>     
> - Un símbolo
>     

Verifica que está corriendo:

```bash
docker ps
```

Si ves algo como:

```
CONTAINER ID   IMAGE                                     STATUS
xxxxxx         mcr.microsoft.com/mssql/server:2019-latest   Up 10 seconds
```

todo está bien ✅

---

## 📦 5. Clonar el proyecto y crear entorno virtual

```bash
git clone https://github.com/Caliz17/api_routeMaster.git  
cd api_routeMaster

python -m venv venv
venv\Scripts\activate
```

> Si ves `(venv)` al inicio del prompt, el entorno virtual está activo.

---

## 📜 6. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## ⚙️ 7. Configurar variables de entorno

Copia el archivo de ejemplo:

```bash
copy .env.example .env
```

Edita el archivo `.env` con tu editor de texto favorito (por ejemplo, VS Code o Notepad):

```env
DATABASE_URL=mssql+pyodbc://sa:YourStrong!Passw0rd@localhost:1433/RouteMasterDB?driver=ODBC+Driver+17+for+SQL+Server
JWT_SECRET_KEY=supersecretkey
JWT_ALGORITHM=HS256
```

> ⚠️ Asegúrate de usar **el mismo password** que configuraste en el contenedor Docker.

---

## 🗄️ 8. Crear base de datos y tablas

Ejecuta:

```bash
python app\scripts\setup_database.py
```

Esto creará la base de datos y las tablas necesarias.

---

## 🌱 9. Sembrar roles y permisos iniciales

```bash
python -m app.scripts.seed_roles
python -m app.scripts.seed_permissions
```

> Si usas PowerShell, asegúrate de estar en la carpeta del proyecto y tener el entorno virtual activo.

---

## 🚀 10. Levantar la API

```bash
uvicorn app.main:app --reload
```

La API quedará corriendo en:  
👉 [http://localhost:8000](http://localhost:8000/)

---

## 📚 11. Ver documentación interactiva

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
    
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
    

---

## 🧠 12. Comandos útiles

|Acción|Comando|
|---|---|
|Ver contenedores activos|`docker ps`|
|Detener contenedor SQL|`docker stop sqlserver`|
|Iniciar contenedor SQL|`docker start sqlserver`|
|Eliminar contenedor SQL|`docker rm -f sqlserver`|
|Eliminar base y tablas (recrear)|`python app\scripts\setup_database.py`|

---

## ✅ Resultado Final

Cuando termines estos pasos tendrás:

- 🧱 SQL Server corriendo en Docker
    
- ⚙️ API FastAPI conectada a la base
    
- 🔑 Roles y permisos preconfigurados
    
- 📚 Documentación Swagger activa
    
- 🚀 Sistema listo para desarrollo
    
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