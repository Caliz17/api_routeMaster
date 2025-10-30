# app/auth/validators.py
import re
from fastapi import HTTPException, status
from app.config.config import settings

def validate_password(password: str):
    """
    Validar fortaleza de contraseña
    """
    # Longitud mínima
    if len(password) < settings.PASSWORD_MIN_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La contraseña debe tener al menos {settings.PASSWORD_MIN_LENGTH} caracteres"
        )
    
    # Longitud máxima
    if len(password) > settings.PASSWORD_MAX_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La contraseña no puede tener más de {settings.PASSWORD_MAX_LENGTH} caracteres"
        )
    
    # Al menos una mayúscula
    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe contener al menos una letra mayúscula"
        )
    
    # Al menos una minúscula
    if not re.search(r"[a-z]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe contener al menos una letra minúscula"
        )
    
    # Al menos un número
    if not re.search(r"\d", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe contener al menos un número"
        )
    
    # Al menos un carácter especial
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe contener al menos un carácter especial (!@#$%^&*(), etc.)"
        )
    
    return True