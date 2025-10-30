from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.config.database import get_db
from app.schemas.user import UserCreate, UserLogin, LoginResponse
from app.auth.utils import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.crud.user import create_user, get_user_by_email, get_user_by_username
from app.auth.dependencies import get_current_active_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=LoginResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Registrar un nuevo usuario
    """
    # Verificar si el email ya existe
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Verificar si el username ya existe
    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya existe"
        )
    
    # Crear usuario
    db_user = create_user(db, user)
    
    # Crear token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        message="Registro exitoso"
    )

@router.post("/login", response_model=LoginResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Iniciar sesión y obtener token JWT
    """
    user = authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        message="Login exitoso"
    )

@router.post("/refresh-token", response_model=LoginResponse)
def refresh_token(current_user=Depends(get_current_active_user)):
    """
    Refrescar token JWT
    """
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.email}, expires_delta=access_token_expires
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        message="Token refrescado exitosamente"
    )