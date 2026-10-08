from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, schemas, security
from app.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)

# 1. Endpoint para registrar un nuevo usuario
@router.post("/registro", response_model=schemas.UsuarioRespuesta, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: schemas.UsuarioCrear, db: Session = Depends(get_db)):
    # Verificar si el email ya existe
    usuario_existente = db.query(models.UsuarioDB).filter(models.UsuarioDB.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado en el sistema."
        )

    # Hashear contraseña y guardar usuario
    hashed_pwd = security.generar_hash_password(usuario.password)
    nuevo_usuario = models.UsuarioDB(
        email=usuario.email,
        hashed_password=hashed_pwd
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


# 2. Endpoint para iniciar sesión y obtener el Token JWT
@router.post("/login", response_model=schemas.Token)
def login_por_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Nota: OAuth2PasswordRequestForm usa la propiedad 'username' para el campo del usuario (usamos email ahí)
    usuario = db.query(models.UsuarioDB).filter(models.UsuarioDB.email == form_data.username).first()
    
    # Validar existencia y contraseña
    if not usuario or not security.verificar_password(form_data.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generar Token JWT con el email del usuario
    access_token = security.crear_token_acceso(data={"sub": usuario.email})
    return {"access_token": access_token, "token_type": "bearer"}