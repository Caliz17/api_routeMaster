from fastapi import FastAPI, Depends
from app.config.database import Base, engine
from app.models.user import User
from app.routes import auth, users
from app.auth.dependencies import get_current_active_user

# Crear tablas
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas correctamente")
except Exception as e:
    print(f"❌ Error creando tablas: {e}")

app = FastAPI(
    title="API",
    description="""
    Sistema de autenticación completo con SQL Server y JWT tokens.
    
    ## Características:
    - ✅ Registro de usuarios
    - ✅ Login con JWT
    - ✅ Rutas protegidas
    - ✅ Gestión de perfiles
    - ✅ Documentación automática
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "ING. SISTEMAS",
        "email": "ecalizc@miumg.edu.gt",
    },
    license_info={
        "name": "MIUMG",
    }
)

# Incluir routers
app.include_router(auth.router)
app.include_router(users.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "¡Hola Mundo!"}

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}

@app.get("/protected", tags=["Test"])
def protected_route(current_user: User = Depends(get_current_active_user)):
    """
    Ruta protegida - solo accesible con token válido
    """
    return {
        "message": "¡Acceso autorizado!",
        "user": current_user.username,
        "email": current_user.email
    }