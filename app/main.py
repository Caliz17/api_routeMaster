from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from app.config.database import Base, engine
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.routes import auth, users, admin, productos, clientes, productos, pedidos, rutas, dashboard

# Crear tablas
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas correctamente")
except Exception as e:
    print(f"❌ Error creando tablas: {e}")

app = FastAPI(
    title="FastAPI Auth API",
    description="Sistema de autenticación con permisos granulares",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ✅ CONFIGURACIÓN PERSONALIZADA DE OPENAPI PARA OCULTAR PARÁMETROS
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Limpiar parámetros automáticos no deseados
    for path, methods in openapi_schema["paths"].items():
        for method, details in methods.items():
            if "parameters" in details:
                # Filtrar solo los parámetros que queremos mostrar
                filtered_params = []
                for param in details["parameters"]:
                    param_name = param.get("name", "")
                    # ✅ MOSTRAR solo skip, limit, user_id y otros parámetros útiles
                    if param_name in ["skip", "limit", "user_id"]:
                        filtered_params.append(param)
                    # ✅ OCULTAR db, token, current_user y otros parámetros internos
                    elif param_name not in ["db", "token", "current_user", "credentials"]:
                        filtered_params.append(param)
                
                details["parameters"] = filtered_params
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Incluir routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(productos.router)
app.include_router(clientes.router)
app.include_router(pedidos.router)
app.include_router(rutas.router)
app.include_router(dashboard.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "¡FastAPI Auth funcionando con SQL Server!"}

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}

@app.get("/protected", tags=["Test"])
def protected_route(current_user: User = Depends(admin.get_current_active_user)):
    """
    Ruta protegida - solo accesible con token válido
    """
    return {
        "message": "¡Acceso autorizado!",
        "user": current_user.username,
        "email": current_user.email
    }