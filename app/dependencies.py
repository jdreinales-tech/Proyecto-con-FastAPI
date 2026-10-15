from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.models import UsuarioDB
from app.routers.auth import get_current_user
from app import models, schemas
from app.database import get_db
from config import settings

# Indica a FastAPI que el token se obtiene de la ruta /auth/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def exigir_rol_admin(current_user: UsuarioDB = Depends(get_current_user)):
    if getattr(current_user, "role", "user") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requieren privilegios de administrador." 
        )
    return current_user


def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.UsuarioDB:
    
    exception_auth = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales de autenticación",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodificar el JWT token usando la clave secreta
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise exception_auth
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise exception_auth

    # Buscar el usuario correspondiente en la base de datos
    usuario = db.query(models.UsuarioDB).filter(models.UsuarioDB.email == token_data.email).first()
    if usuario is None:
        raise exception_auth
        
    return usuario