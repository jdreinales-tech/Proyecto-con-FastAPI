from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List

# ---------------------------------------------------------
# ESQUEMAS DE USUARIO
# ---------------------------------------------------------
class UsuarioCrear(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="Contraseña de mínimo 6 caracteres")

class UsuarioRespuesta(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------
# ESQUEMAS DE LIBROS
# ---------------------------------------------------------
class LibroBase(BaseModel):
    titulo: str = Field(..., min_length=2, max_length=100, description="Título del libro")
    autor: str = Field(..., min_length=2, max_length=50, description="Autor del libro")

class LibroCrear(LibroBase):
    pass

class Libro(LibroBase):
    id: int
    prestado: bool
    usuario_id: int
    # Incluimos los datos del propietario usando el esquema de respuesta
    propietario: UsuarioRespuesta 

    model_config = ConfigDict(from_attributes=True)


# Extendemos UsuarioRespuesta para incluir sus libros creados si lo necesitamos
class UsuarioConLibros(UsuarioRespuesta):
    libros: List[LibroBase] = []


# ---------------------------------------------------------
# ESQUEMAS DE TOKENS JWT
# ---------------------------------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None