from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class UsuarioDB(Base):
    __tablename__="usuarios"

    id=Column(Integer, primary_key=True, index=True)
    email=Column(String, unique=True, index=True)
    hashed_password=Column(String)
    is_active=Column(Boolean, default=True)
    role=Column(String, default="user")
    libros=relationship("LibroDB", back_populates="propietario")

class LibroDB(Base):
    __tablename__="libros"

    id=Column(Integer, primary_key=True, index=True)
    titulo=Column(String,index=True)
    autor=Column(String, index=True)
    prestado=Column(Boolean, default=False)
    usuario_id=Column(Integer, ForeignKey("usuarios.id"))
    propietario=relationship("UsuarioDB", back_populates="libros")